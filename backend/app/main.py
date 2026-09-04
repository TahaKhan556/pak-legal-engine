from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.api.v1 import search, documents, contributors, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Kanun - Legal Knowledge Engine",
    description="Pakistani Law Search & Plain-Language Legal Answers",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api/v1/search", tags=["Search"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(contributors.router, prefix="/api/v1/contribute", tags=["Contributors"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "kanun-legal-engine"}
