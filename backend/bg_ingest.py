#!/usr/bin/env python3
"""Background ingestion - writes progress to file."""
import hashlib
import re
import json
import time
from pathlib import Path

PROGRESS_FILE = "/tmp/kanun_ingest_progress.json"

def log(msg):
    with open("/tmp/kanun_ingest.log", "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")
    print(msg, flush=True)

log("Starting background ingestion...")

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, PayloadSchemaType
from sentence_transformers import SentenceTransformer
from datasets import load_dataset

log("Loading model...")
model = SentenceTransformer("BAAI/bge-base-en-v1.5")
log("Model loaded")

log("Connecting to Qdrant...")
client = QdrantClient(host="localhost", port=6333)

try:
    client.delete_collection("legal_docs")
    log("Deleted old collection")
except:
    pass

log("Creating collection...")
client.create_collection(
    collection_name="legal_docs",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    on_disk_payload=True,
)
client.create_payload_index(collection_name="legal_docs", field_name="doc_type", field_schema=PayloadSchemaType.KEYWORD)
client.create_payload_index(collection_name="legal_docs", field_name="province", field_schema=PayloadSchemaType.KEYWORD)
client.create_payload_index(collection_name="legal_docs", field_name="year", field_schema=PayloadSchemaType.INTEGER)

log("Loading dataset...")
dataset = load_dataset("endomorphosis/ipfs_pakistan_laws", split="train")
log(f"Loaded {len(dataset)} laws")

total_chunks = 0
batch_points = []

def flush_batch():
    global batch_points
    if batch_points:
        client.upsert(collection_name="legal_docs", points=batch_points)
        batch_points = []

for idx, row in enumerate(dataset):
    title = str(row.get("title", "") or "")
    text = str(row.get("text", "") or "")
    
    if not text or len(text) < 50:
        continue
    
    # Simple chunking
    chunks = []
    for i in range(0, min(len(text), 50000), 700):
        chunk = text[i:i+768]
        if len(chunk) > 20:
            chunks.append(chunk)
    
    if not chunks:
        continue
    
    # Infer metadata
    t = title.lower()
    if "constitution" in t: doc_type = "constitution"
    elif "penal code" in t: doc_type = "ppc"
    elif "criminal procedure" in t: doc_type = "crpc"
    elif "civil procedure" in t: doc_type = "cpc"
    elif "ordinance" in t: doc_type = "ordinance"
    elif "act" in t: doc_type = "federal_act"
    else: doc_type = "federal_act"
    
    year_match = re.search(r',?\s*(\d{4})', title)
    year = int(year_match.group(1)) if year_match and 1800 <= int(year_match.group(1)) <= 2030 else None
    
    source_url = str(row.get("source_url", "") or "")
    
    for ci, chunk in enumerate(chunks):
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
        batch_points.append(point)
        total_chunks += 1
    
    # Flush every 25 laws
    if (idx + 1) % 25 == 0:
        flush_batch()
        progress = {"laws": idx + 1, "total": len(dataset), "chunks": total_chunks, "status": "running"}
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress, f)
        log(f"Progress: {idx+1}/{len(dataset)} laws, {total_chunks} chunks")

flush_batch()
info = client.get_collection("legal_docs")
progress = {"laws": len(dataset), "total": len(dataset), "chunks": total_chunks, "points": info.points_count, "status": "done"}
with open(PROGRESS_FILE, "w") as f:
    json.dump(progress, f)
log(f"DONE! {info.points_count} points indexed")
