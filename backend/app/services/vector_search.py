from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range
from sentence_transformers import SentenceTransformer
from typing import Optional
import threading

from app.config import settings


_model_lock = threading.Lock()
_model_instance = None


def _get_model() -> SentenceTransformer:
    global _model_instance
    if _model_instance is None:
        with _model_lock:
            if _model_instance is None:
                _model_instance = SentenceTransformer("BAAI/bge-base-en-v1.5")
    return _model_instance


class VectorSearchService:
    MIN_SCORE = 0.68

    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )
        self.collection = "legal_docs"
        self._optimized = False

    def _ensure_optimized(self):
        if not self._optimized:
            try:
                self.client.optimize(collection_name=self.collection, wait=True)
                self._optimized = True
            except Exception:
                pass

    async def search(
        self,
        query: str,
        province: Optional[str] = None,
        doc_type: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        limit: int = 5,
    ) -> list[dict]:
        self._ensure_optimized()
        model = _get_model()
        query_embedding = model.encode(query).tolist()

        must_conditions = []

        if province:
            must_conditions.append(
                FieldCondition(key="province", match=MatchValue(value=province))
            )
        if doc_type:
            must_conditions.append(
                FieldCondition(key="doc_type", match=MatchValue(value=doc_type))
            )
        if year_from or year_to:
            year_range = {}
            if year_from:
                year_range["gte"] = year_from
            if year_to:
                year_range["lte"] = year_to
            must_conditions.append(
                FieldCondition(key="year", range=Range(**year_range))
            )

        query_filter = Filter(must=must_conditions) if must_conditions else None

        results = self.client.query_points(
            collection_name=self.collection,
            query=query_embedding,
            query_filter=query_filter,
            limit=min(limit * 3, 30),
            with_payload=True,
        )

        filtered = [
            {
                "id": str(point.id),
                "score": point.score,
                "payload": point.payload,
            }
            for point in results.points
            if point.score >= self.MIN_SCORE
        ]

        seen_titles = set()
        deduped = []
        for r in filtered:
            title = r["payload"].get("title", "")
            if title not in seen_titles:
                seen_titles.add(title)
                deduped.append(r)

        return deduped[:limit]

    async def get_collection_info(self) -> dict:
        info = self.client.get_collection(self.collection)
        return {
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "status": str(info.status),
        }
