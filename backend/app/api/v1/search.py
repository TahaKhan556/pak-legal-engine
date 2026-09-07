from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.search import SearchRequest, SearchResponse, SearchResult
from app.services.vector_search import VectorSearchService
from app.services.llm_service import LLMService
from app.services.query_enhancer import enhance_query
from app.models.document import SearchLog

router = APIRouter()

_vector_service = None
_llm_service = None


def _get_vector_service() -> VectorSearchService:
    global _vector_service
    if _vector_service is None:
        _vector_service = VectorSearchService()
    return _vector_service


def _get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


@router.post("", response_model=SearchResponse)
async def search_laws(request: SearchRequest, db: AsyncSession = Depends(get_db)):
    vector_svc = _get_vector_service()
    llm_svc = _get_llm_service()

    enhanced = await enhance_query(request.query)

    all_results = []
    seen_ids = set()

    for search_q in enhanced["search_queries"]:
        if not search_q.strip():
            continue
        results = await vector_svc.search(
            query=search_q,
            province=request.province,
            doc_type=request.doc_type,
            year_from=request.year_from,
            year_to=request.year_to,
            limit=7,
        )
        for r in results:
            if r["id"] not in seen_ids:
                seen_ids.add(r["id"])
                all_results.append(r)

    all_results.sort(key=lambda x: x["score"], reverse=True)
    top_results = all_results[:5]

    search_results = [
        SearchResult(
            id=r["id"],
            title=r["payload"].get("title", ""),
            section=r["payload"].get("section", ""),
            content=r["payload"].get("chunk_text", ""),
            score=r["score"],
            doc_type=r["payload"].get("doc_type", ""),
            province=r["payload"].get("province", ""),
            year=r["payload"].get("year"),
            source_url=r["payload"].get("source_url", ""),
        )
        for r in top_results
    ]

    context = "\n\n".join([
        f"--- {r.title} ({r.section}) ---\n{r.content[:1200]}"
        for r in search_results
    ])

    llm_response = await llm_svc.generate_legal_answer(
        query=enhanced["english"],
        context=context,
    )

    log = SearchLog(
        query=request.query,
        results_count=len(search_results),
    )
    db.add(log)
    await db.commit()

    return SearchResponse(
        query=request.query,
        verdict=llm_response.get("verdict", ""),
        legal_references=search_results,
        steps=llm_response.get("steps", []),
        plain_language=llm_response.get("plain_language", ""),
        plain_urdu=llm_response.get("plain_urdu", ""),
    )


@router.get("/suggestions")
async def get_suggestions(q: str = "", limit: int = 5):
    common_queries = [
        "Can police check my phone without a warrant?",
        "What are my rights during arrest?",
        "How to file an FIR in Pakistan?",
        "What is the punishment for theft under PPC?",
        "Can my landlord evict me without notice?",
        "What to do if someone cyber harasses me?",
        "How to get bail in a criminal case?",
        "What are fundamental rights in the Constitution of Pakistan?",
        "Can anyone file an FIR without evidence?",
        "What is PECA and how does it protect me online?",
    ]

    if q:
        filtered = [s for s in common_queries if q.lower() in s.lower()]
        if not filtered:
            filtered = common_queries[:limit]
        return filtered[:limit]

    return common_queries[:limit]
