from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class SearchRequest(BaseModel):
    query: str
    province: Optional[str] = None
    doc_type: Optional[str] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    limit: int = 10


class SearchResult(BaseModel):
    id: str
    title: str
    section: str
    content: str
    score: float
    doc_type: str
    province: str
    year: Optional[int]
    source_url: Optional[str]


class SearchResponse(BaseModel):
    query: str
    verdict: str
    legal_references: list[SearchResult]
    steps: list[str]
    plain_language: str
    plain_urdu: str


class DocumentResponse(BaseModel):
    id: UUID
    title: str
    title_urdu: Optional[str]
    document_type: str
    province: str
    year: Optional[int]
    description: Optional[str]
    total_sections: int
    source_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class SectionResponse(BaseModel):
    id: UUID
    section_number: str
    title: Optional[str]
    content: str
    plain_english: Optional[str]
    plain_urdu: Optional[str]
    keywords: Optional[list[str]]

    class Config:
        from_attributes = True


class ContributorCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str]
    organization: Optional[str]


class ContributionCreate(BaseModel):
    contributor: ContributorCreate
    document_type: Optional[str]
    title: str
    content: Optional[str]


class ContributionResponse(BaseModel):
    id: UUID
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    total_documents: int
    total_sections: int
    documents_by_type: dict[str, int]
    documents_by_province: dict[str, int]
