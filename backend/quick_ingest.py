#!/usr/bin/env python3
"""Quick ingestion script for Pakistan Laws Dataset."""
import sys
import os
import hashlib
import re
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
os.chdir(Path(__file__).parent.parent)

# Force unbuffered output
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

print("Starting ingestion...", flush=True)

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, PayloadSchemaType
print("Qdrant client imported", flush=True)

from sentence_transformers import SentenceTransformer
print("Sentence transformers imported", flush=True)

def chunk_text(text, chunk_size=768, overlap=128):
    if not text or len(text) < 100:
        return [text] if text else []
    parts = re.split(r'\n\n|\n(?=Section|Article|Chapter)', text)
    chunks = []
    current = ""
    for part in parts:
        if len(current) + len(part) < chunk_size:
            current += (" " if current else "") + part
        else:
            if current.strip():
                chunks.append(current.strip())
            current = part
    if current.strip():
        chunks.append(current.strip())
    return chunks if chunks else [text[:chunk_size]]

def infer_type(title):
    t = title.lower() if title else ""
    if "constitution" in t: return "constitution"
    if "penal code" in t: return "ppc"
    if "criminal procedure" in t: return "crpc"
    if "civil procedure" in t: return "cpc"
    if "ordinance" in t: return "ordinance"
    if "act" in t: return "federal_act"
    return "federal_act"

def infer_year(title):
    m = re.search(r',?\s*(\d{4})', title or "")
    if m:
        y = int(m.group(1))
        if 1800 <= y <= 2030:
            return y
    return None

print("Loading model...", flush=True)
model = SentenceTransformer("BAAI/bge-base-en-v1.5")
print("Model loaded", flush=True)

print("Connecting to Qdrant...", flush=True)
client = QdrantClient(host="localhost", port=6333)

try:
    client.delete_collection("legal_docs")
    print("Deleted old collection", flush=True)
except:
    pass

print("Creating collection...", flush=True)
client.create_collection(
    collection_name="legal_docs",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    on_disk_payload=True,
)
client.create_payload_index(collection_name="legal_docs", field_name="doc_type", field_schema=PayloadSchemaType.KEYWORD)
client.create_payload_index(collection_name="legal_docs", field_name="province", field_schema=PayloadSchemaType.KEYWORD)
client.create_payload_index(collection_name="legal_docs", field_name="year", field_schema=PayloadSchemaType.INTEGER)
print("Collection created with indexes", flush=True)

print("Loading dataset...", flush=True)
from datasets import load_dataset
dataset = load_dataset("endomorphosis/ipfs_pakistan_laws", split="train")
print(f"Loaded {len(dataset)} laws", flush=True)

points = []
total_chunks = 0

for idx, row in enumerate(dataset):
    title = str(row.get("title", "") or "")
    text = str(row.get("text", "") or "")
    
    if not text or len(text) < 50:
        continue
    
    doc_type = infer_type(title)
    year = infer_year(title)
    source_url = str(row.get("source_url", "") or "")
    
    chunks = chunk_text(text)
    
    for ci, chunk in enumerate(chunks):
        if len(chunk) < 20:
            continue
        embedding = model.encode(chunk).tolist()
        point = PointStruct(
            id=hashlib.md5(f"{idx}_{ci}_{chunk[:50]}".encode()).hexdigest(),
            vector=embedding,
            payload={
                "doc_id": str(row.get("id", idx)),
                "title": title,
                "doc_type": doc_type,
                "province": "federal",
                "year": year,
                "section": f"Chunk {ci+1}",
                "chunk_text": chunk,
                "source_url": source_url,
                "keywords": [],
            },
        )
        points.append(point)
        total_chunks += 1
    
    if len(points) >= 50:
        client.upsert(collection_name="legal_docs", points=points)
        points = []
    
    if (idx + 1) % 50 == 0:
        print(f"Processed {idx+1}/{len(dataset)} laws ({total_chunks} chunks)", flush=True)

if points:
    client.upsert(collection_name="legal_docs", points=points)

info = client.get_collection("legal_docs")
print(f"\nDONE! {info.points_count} points indexed", flush=True)
