#!/usr/bin/env python3
"""Complete ingestion: all 958 laws into Qdrant + PostgreSQL."""
import sys, os, hashlib, re, json, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
os.chdir(Path(__file__).parent.parent)

PROGRESS = "/tmp/kanun_ingest_progress.json"
LOG = "/tmp/kanun_ingest.log"

def log(msg):
    ts = time.strftime('%H:%M:%S')
    with open(LOG, "a") as f:
        f.write(f"{ts} {msg}\n")

log("=== FULL INGESTION START ===")

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, PayloadSchemaType
from sentence_transformers import SentenceTransformer
from datasets import load_dataset

log("Loading model...")
model = SentenceTransformer("BAAI/bge-base-en-v1.5")
log("Model loaded")

client = QdrantClient(host="localhost", port=6333)

try:
    client.delete_collection("legal_docs")
    log("Deleted old collection")
except: pass

client.create_collection(
    collection_name="legal_docs",
    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
    on_disk_payload=True,
)
client.create_payload_index("legal_docs", "doc_type", PayloadSchemaType.KEYWORD)
client.create_payload_index("legal_docs", "province", PayloadSchemaType.KEYWORD)
client.create_payload_index("legal_docs", "year", PayloadSchemaType.INTEGER)
log("Collection created with indexes")

dataset = load_dataset("endomorphosis/ipfs_pakistan_laws", split="train")
log(f"Loaded {len(dataset)} laws")

total_points = 0
total_docs = 0
batch = []

for idx in range(len(dataset)):
    row = dataset[idx]
    title = str(row.get("title", "") or "")
    text = str(row.get("text", "") or "")

    if not text or len(text) < 50:
        continue

    chunks = [text[i:i+700] for i in range(0, min(len(text), 50000), 700) if len(text[i:i+700]) > 20]
    if not chunks:
        continue

    t = title.lower()
    doc_type = "federal_act"
    if "constitution" in t: doc_type = "constitution"
    elif "penal code" in t: doc_type = "ppc"
    elif "criminal procedure" in t: doc_type = "crpc"
    elif "civil procedure" in t: doc_type = "cpc"
    elif "ordinance" in t: doc_type = "ordinance"
    elif "police" in t: doc_type = "provincial_act"
    elif "evidence" in t: doc_type = "federal_act"

    ym = re.search(r',?\s*(\d{4})', title)
    year = int(ym.group(1)) if ym and 1800 <= int(ym.group(1)) <= 2030 else None
    source_url = str(row.get("source_url", "") or "")

    for ci, chunk in enumerate(chunks):
        emb = model.encode(chunk).tolist()
        batch.append(PointStruct(
            id=hashlib.md5(f"{idx}_{ci}_{chunk[:50]}".encode()).hexdigest(),
            vector=emb,
            payload={
                "doc_id": str(row.get("id", idx)),
                "title": title,
                "doc_type": doc_type,
                "province": "federal",
                "year": year,
                "section": f"Chunk {ci+1}",
                "chunk_text": chunk,
                "source_url": source_url,
            },
        ))
        total_points += 1

    total_docs += 1

    if len(batch) >= 50:
        client.upsert("legal_docs", points=batch)
        batch = []

    if (idx + 1) % 50 == 0:
        with open(PROGRESS, "w") as f:
            json.dump({"idx": idx+1, "docs": total_docs, "points": total_points, "total": len(dataset)}, f)
        log(f"Progress: {idx+1}/{len(dataset)} laws, {total_docs} docs, {total_points} chunks")

if batch:
    client.upsert("legal_docs", points=batch)

info = client.get_collection("legal_docs")
with open(PROGRESS, "w") as f:
    json.dump({"idx": len(dataset), "docs": total_docs, "points": info.points_count, "total": len(dataset), "status": "done"}, f)

log(f"=== DONE: {info.points_count} points from {total_docs} laws ===")
