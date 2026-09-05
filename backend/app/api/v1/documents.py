from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.models.document import Document, Section
from app.schemas.search import DocumentResponse, SectionResponse, StatsResponse

router = APIRouter()


@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: AsyncSession = Depends(get_db)):
    total_docs = await db.execute(select(func.count(Document.id)))
    total_sections = await db.execute(select(func.count(Section.id)))

    docs_by_type = await db.execute(
        select(Document.document_type, func.count(Document.id))
        .group_by(Document.document_type)
    )
    docs_by_province = await db.execute(
        select(Document.province, func.count(Document.id))
        .group_by(Document.province)
    )

    return StatsResponse(
        total_documents=total_docs.scalar() or 0,
        total_sections=total_sections.scalar() or 0,
        documents_by_type={str(row[0]): row[1] for row in docs_by_type.all()},
        documents_by_province={str(row[0]): row[1] for row in docs_by_province.all()},
    )


@router.get("/categories/list")
async def get_categories():
    return [
        {"value": "constitution", "label": "Constitution"},
        {"value": "ppc", "label": "Pakistan Penal Code"},
        {"value": "crpc", "label": "Code of Criminal Procedure"},
        {"value": "cpc", "label": "Code of Civil Procedure"},
        {"value": "federal_act", "label": "Federal Acts"},
        {"value": "provincial_act", "label": "Provincial Acts"},
        {"value": "ordinance", "label": "Ordinances"},
        {"value": "rules", "label": "Rules"},
        {"value": "sro", "label": "Statutory Regulatory Orders"},
        {"value": "notification", "label": "Notifications"},
    ]


@router.get("/provinces/list")
async def get_provinces():
    return [
        {"value": "federal", "label": "Federal"},
        {"value": "sindh", "label": "Sindh"},
        {"value": "punjab", "label": "Punjab"},
        {"value": "kpk", "label": "Khyber Pakhtunkhwa"},
        {"value": "balochistan", "label": "Balochistan"},
        {"value": "islamabad", "label": "Islamabad Capital Territory"},
    ]


@router.get("", response_model=list[DocumentResponse])
async def list_documents(
    doc_type: Optional[str] = Query(None),
    province: Optional[str] = Query(None),
    year_from: Optional[int] = Query(None),
    year_to: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    query = select(Document).where(Document.status == "active")

    if doc_type:
        query = query.where(Document.document_type == doc_type)
    if province:
        query = query.where(Document.province == province)
    if year_from:
        query = query.where(Document.year >= year_from)
    if year_to:
        query = query.where(Document.year <= year_to)
    if search:
        query = query.where(Document.title.ilike(f"%{search}%"))

    query = query.offset((page - 1) * limit).limit(limit)

    result = await db.execute(query)
    documents = result.scalars().all()

    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).where(Document.id == document_id))
    document = result.scalar_one_or_none()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document


@router.get("/{document_id}/sections", response_model=list[SectionResponse])
async def get_document_sections(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Section).where(Section.document_id == document_id)
    )
    sections = result.scalars().all()

    return sections
