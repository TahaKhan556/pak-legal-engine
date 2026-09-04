#!/usr/bin/env python3
"""
Bulk ingestion script for HuggingFace Pakistan Laws Dataset.
Downloads and indexes 958+ federal laws into Qdrant vector database.
"""

import sys
import os
import hashlib
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, PayloadSchemaType
from sentence_transformers import SentenceTransformer


def chunk_legal_text(text: str, chunk_size: int = 768, overlap: int = 128) -> list[str]:
    """Split legal text into chunks respecting structure."""
    if not text or len(text) < 100:
        return [text] if text else []

    separators = [
        r'\n\n## ',
        r'\n### ',
        r'\n\n',
        r'\n',
        r'(?<=\.)\s+',
    ]

    chunks = []
    current_chunk = ""

    for separator in separators:
        parts = re.split(separator, text)

        for part in parts:
            if len(current_chunk) + len(part) < chunk_size:
                current_chunk += (" " if current_chunk else "") + part
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = part

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    if not chunks:
        chunks = [text[:chunk_size]]

    return chunks


def extract_keywords(text: str) -> list[str]:
    """Extract legal keywords from text."""
    legal_terms = [
        'article', 'section', 'clause', 'sub-clause', 'proviso',
        'penalty', 'punishment', 'offence', 'crime', 'bail',
        'warrant', 'arrest', 'detention', 'trial', 'appeal',
        'constitutional', 'fundamental rights', 'directive principles',
        'murder', 'theft', 'fraud', 'harassment', 'assault',
        'property', 'contract', 'marriage', 'divorce', 'custody',
        'police', 'court', 'judge', 'magistrate', 'jury',
    ]

    text_lower = text.lower()
    keywords = [term for term in legal_terms if term in text_lower]

    return keywords[:10]


def infer_doc_type(title: str, content: str) -> str:
    """Infer document type from title and content."""
    title_lower = title.lower() if title else ""
    content_lower = content[:500].lower() if content else ""

    if "constitution" in title_lower:
        return "constitution"
    elif "penal code" in title_lower or "ppc" in title_lower:
        return "ppc"
    elif "criminal procedure" in title_lower or "crpc" in title_lower:
        return "crpc"
    elif "civil procedure" in title_lower or "cpc" in title_lower:
        return "cpc"
    elif "ordinance" in title_lower:
        return "ordinance"
    elif "act" in title_lower:
        return "federal_act"
    elif "rules" in title_lower:
        return "rules"
    elif "regulation" in title_lower:
        return "rules"
    else:
        return "federal_act"


def infer_year(title: str, content: str) -> int | None:
    """Try to infer year from title or content."""
    patterns = [
        r',?\s*(\d{4})',
        r'(\d{4})\s*$',
        r'of\s+(\d{4})',
        r'act\s+(\d{4})',
    ]

    for text in [title, content[:1000] if content else ""]:
        if not text:
            continue
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                year = int(match.group(1))
                if 1800 <= year <= 2030:
                    return year

    return None


def main():
    print("=" * 60)
    print("KANUN - Pakistan Laws Dataset Ingestion")
    print("=" * 60)

    print("\n1. Loading BGE embedding model...")
    model = SentenceTransformer("BAAI/bge-base-en-v1.5")
    print("   Model loaded successfully!")

    print("\n2. Connecting to Qdrant...")
    client = QdrantClient(host="localhost", port=6333)

    collections = [c.name for c in client.get_collections().collections]
    if "legal_docs" in collections:
        print("   Collection 'legal_docs' already exists, deleting...")
        client.delete_collection("legal_docs")

    print("   Creating collection 'legal_docs'...")
    client.create_collection(
        collection_name="legal_docs",
        vectors_config=VectorParams(
            size=768,
            distance=Distance.COSINE,
        ),
        on_disk_payload=True,
    )

    print("   Creating payload indexes...")
    client.create_payload_index(
        collection_name="legal_docs",
        field_name="doc_type",
        field_schema=PayloadSchemaType.KEYWORD,
    )
    client.create_payload_index(
        collection_name="legal_docs",
        field_name="province",
        field_schema=PayloadSchemaType.KEYWORD,
    )
    client.create_payload_index(
        collection_name="legal_docs",
        field_name="year",
        field_schema=PayloadSchemaType.INTEGER,
    )

    print("\n3. Downloading HuggingFace dataset...")
    from datasets import load_dataset

    dataset = load_dataset("endomorphosis/ipfs_pakistan_laws", split="train")
    print(f"   Loaded {len(dataset)} laws")

    print("\n4. Processing and indexing laws...")
    points = []
    batch_size = 50
    total_chunks = 0
    skipped = 0

    for idx, row in enumerate(dataset):
        title = str(row.get("title", "") or "")
        text = str(row.get("text", "") or "")

        if not text or len(text) < 50:
            skipped += 1
            continue

        doc_type = infer_doc_type(title, text)
        year = infer_year(title, text)
        source_url = str(row.get("source_url", "") or "")

        chunks = chunk_legal_text(text)

        for chunk_idx, chunk in enumerate(chunks):
            if len(chunk) < 20:
                continue

            embedding = model.encode(chunk).tolist()
            keywords = extract_keywords(chunk)

            point_id = hashlib.md5(
                f"{idx}_{chunk_idx}_{chunk[:50]}".encode()
            ).hexdigest()

            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "doc_id": str(row.get("id", idx)),
                    "title": title,
                    "doc_type": doc_type,
                    "province": "federal",
                    "year": year,
                    "section": f"Chunk {chunk_idx + 1}",
                    "chunk_text": chunk,
                    "source_url": source_url,
                    "keywords": keywords,
                },
            )
            points.append(point)
            total_chunks += 1

        if len(points) >= batch_size:
            client.upsert(collection_name="legal_docs", points=points)
            points = []
            if (idx + 1) % 100 == 0:
                print(f"   Processed {idx + 1}/{len(dataset)} laws ({total_chunks} chunks)")

    if points:
        client.upsert(collection_name="legal_docs", points=points)

    print(f"\n5. Ingestion complete!")
    print(f"   Laws processed: {len(dataset) - skipped}")
    print(f"   Laws skipped: {skipped}")
    print(f"   Total chunks indexed: {total_chunks}")

    info = client.get_collection("legal_docs")
    print(f"   Qdrant points: {info.points_count}")

    print("\n" + "=" * 60)
    print("DONE! Legal knowledge base is ready.")
    print("=" * 60)


if __name__ == "__main__":
    main()
