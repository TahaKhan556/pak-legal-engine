from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.schemas.search import SearchRequest, SearchResponse, SearchResult
from app.services.vector_search import VectorSearchService
from app.services.llm_service import LLMService
from app.models.document import SearchLog

router = APIRouter()


@router.post("", response_model=SearchResponse)
async def search_laws(request: SearchRequest, db: AsyncSession = Depends(get_db)):
    vector_service = VectorSearchService()
    llm_service = LLMService()

    results = await vector_service.search(
        query=request.query,
        province=request.province,
        doc_type=request.doc_type,
        year_from=request.year_from,
        year_to=request.year_to,
        limit=request.limit,
    )

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
        for r in results
    ]

    context = "\n\n".join([f"--- {r.title} ({r.section}) ---\n{r.content}" for r in search_results[:5]])

    llm_response = await llm_service.generate_legal_answer(
        query=request.query,
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
        "How to file an FIR?",
        "What is the punishment for theft?",
        "Can my landlord evict me without notice?",
        "What to do if cyber harassed?",
        "How to get bail?",
        "What are fundamental rights in Pakistan?",
    ]

    if q:
        filtered = [s for s in common_queries if q.lower() in s.lower()]
        return filtered[:limit]

    return common_queries[:limit]
