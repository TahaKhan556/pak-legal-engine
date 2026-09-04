from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range
from sentence_transformers import SentenceTransformer
from typing import Optional
import os

from app.config import settings


class VectorSearchService:
    def __init__(self):
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )
        self.model = SentenceTransformer("BAAI/bge-base-en-v1.5")
        self.collection = "legal_docs"

    async def search(
        self,
        query: str,
        province: Optional[str] = None,
        doc_type: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        limit: int = 10,
    ) -> list[dict]:
        query_embedding = self.model.encode(query).tolist()

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
            limit=limit,
            with_payload=True,
        )

        return [
            {
                "id": str(point.id),
                "score": point.score,
                "payload": point.payload,
            }
            for point in results.points
        ]

    async def get_collection_info(self) -> dict:
        info = self.client.get_collection(self.collection)
        return {
            "vectors_count": info.vectors_count,
            "points_count": info.points_count,
            "status": str(info.status),
        }
