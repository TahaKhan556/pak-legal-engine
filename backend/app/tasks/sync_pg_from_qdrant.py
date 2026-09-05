#!/usr/bin/env python3
"""Sync PostgreSQL from Qdrant vector database."""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
os.chdir(Path(__file__).parent.parent)

import asyncio
from collections import defaultdict
from qdrant_client import QdrantClient
from app.database import AsyncSessionLocal
from app.models.document import Document, Section
from app.models.document import DocumentType, Province


def infer_doc_type(title: str) -> str:
    t = title.lower() if title else ""
    if "constitution" in t: return "constitution"
    if "penal code" in t: return "ppc"
    if "criminal procedure" in t: return "crpc"
    if "civil procedure" in t: return "cpc"
    if "ordinance" in t: return "ordinance"
    if "act" in t: return "federal_act"
    if "rules" in t: return "rules"
    return "federal_act"


def infer_year(title: str) -> int | None:
    import re
    m = re.search(r',?\s*(\d{4})', title or "")
    if m:
        y = int(m.group(1))
        if 1800 <= y <= 2030:
            return y
    return None


async def main():
    print("Connecting to Qdrant...")
    client = QdrantClient(host="localhost", port=6333)

    info = client.get_collection("legal_docs")
    print(f"Qdrant has {info.points_count} points")

    print("Fetching all points...")
    all_points = []
    offset = None
    while True:
        result = client.scroll(
            collection_name="legal_docs",
            limit=100,
            offset=offset,
            with_payload=True,
        )
        points, next_offset = result
        all_points.extend(points)
        if next_offset is None or len(points) == 0:
            break
        offset = next_offset

    print(f"Fetched {len(all_points)} points")

    docs_map = defaultdict(lambda: {"chunks": [], "title": "", "doc_type": "", "province": "federal", "year": None, "source_url": ""})

    for point in all_points:
        payload = point.payload
        title = payload.get("title", "Unknown")
        if not docs_map[title]["title"]:
            docs_map[title]["title"] = title
            docs_map[title]["doc_type"] = payload.get("doc_type", "federal_act")
            docs_map[title]["province"] = payload.get("province", "federal")
            docs_map[title]["year"] = payload.get("year")
            docs_map[title]["source_url"] = payload.get("source_url", "")
        docs_map[title]["chunks"].append({
            "section_number": payload.get("section", ""),
            "content": payload.get("chunk_text", ""),
        })

    print(f"Grouped into {len(docs_map)} unique documents")

    print("Writing to PostgreSQL...")
    async with AsyncSessionLocal() as session:
        async with session.begin():
            existing = await session.execute(select(Document.id))
            if existing.scalars().first():
                print("PostgreSQL already has documents, skipping...")
                return

            for title, doc_data in docs_map.items():
                doc = Document(
                    title=title,
                    document_type=doc_data["doc_type"],
                    province=doc_data["province"],
                    year=doc_data["year"],
                    source_url=doc_data["source_url"],
                    status="active",
                    total_sections=len(doc_data["chunks"]),
                )
                session.add(doc)
                await session.flush()

                for chunk in doc_data["chunks"]:
                    section = Section(
                        document_id=doc.id,
                        section_number=chunk["section_number"],
                        content=chunk["content"],
                    )
                    session.add(section)

    print(f"Done! Inserted {len(docs_map)} documents into PostgreSQL")


if __name__ == "__main__":
    from sqlalchemy import select
    asyncio.run(main())
