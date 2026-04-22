"""
Phase 2 — Embedding + Pinecone Index
Reads chunks.jsonl, embeds with all-MiniLM-L6-v2, upserts into Pinecone.
"""

import os
import json
import logging
from pathlib import Path

import yaml
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config + secrets
# ---------------------------------------------------------------------------

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

with open(ROOT / "config.yaml") as f:
    CFG = yaml.safe_load(f)

CHUNKS_FILE  = ROOT / CFG["ingestion"]["output_dir"] / CFG["ingestion"]["output_file"]
EMB_MODEL    = CFG["embedding"]["model"]
BATCH_SIZE   = CFG["embedding"]["batch_size"]

VS           = CFG["vector_store"]
INDEX_NAME   = VS["index_name"]
NAMESPACE    = VS["namespace"]
DIMENSION    = VS["dimension"]
METRIC       = VS["metric"]
CLOUD        = VS["cloud"]
REGION       = VS["region"]

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if not PINECONE_API_KEY:
    raise EnvironmentError("PINECONE_API_KEY not set — copy .env.example to .env and fill it in")


# ---------------------------------------------------------------------------
# Connect to Pinecone
# ---------------------------------------------------------------------------

def get_or_create_index(pc: Pinecone):
    existing = [idx.name for idx in pc.list_indexes()]
    if INDEX_NAME not in existing:
        log.info("Creating Pinecone index '%s' ...", INDEX_NAME)
        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            metric=METRIC,
            spec=ServerlessSpec(cloud=CLOUD, region=REGION),
        )
        log.info("Index created.")
    else:
        log.info("Index '%s' already exists — reusing.", INDEX_NAME)
    return pc.Index(INDEX_NAME)


# ---------------------------------------------------------------------------
# Embed + upsert
# ---------------------------------------------------------------------------

def load_chunks() -> list[dict]:
    chunks = []
    with open(CHUNKS_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


def build_pinecone_vectors(chunks: list[dict], embeddings: list[list[float]]) -> list[dict]:
    vectors = []
    for chunk, embedding in zip(chunks, embeddings):
        vectors.append({
            "id":     chunk["id"],
            "values": embedding,
            "metadata": {
                "source":      chunk["source"],
                "chunk_index": chunk["chunk_index"],
                "tokens":      chunk["tokens"],
                "text":        chunk["text"],          # stored for retrieval
                "ingested_at": chunk["metadata"]["ingested_at"],
            }
        })
    return vectors


def upsert_in_batches(index, vectors: list[dict], batch_size: int):
    total = len(vectors)
    for i in range(0, total, batch_size):
        batch = vectors[i: i + batch_size]
        index.upsert(vectors=batch, namespace=NAMESPACE)
        log.info("  Upserted %d / %d vectors", min(i + batch_size, total), total)


# ---------------------------------------------------------------------------
# Test query
# ---------------------------------------------------------------------------

def test_query(index, model: SentenceTransformer, question: str):
    log.info("\nTest query: '%s'", question)
    q_vec = model.encode([question])[0].tolist()
    results = index.query(
        vector=q_vec,
        top_k=3,
        namespace=NAMESPACE,
        include_metadata=True,
    )
    print("\n" + "="*60)
    print(f"Query: {question}")
    print("="*60)
    for match in results["matches"]:
        score  = match["score"]
        source = match["metadata"]["source"]
        text   = match["metadata"]["text"][:200]
        print(f"\n  Score : {score:.4f}")
        print(f"  Source: {source}")
        print(f"  Text  : {text}...")
    print("="*60 + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run():
    log.info("Loading chunks from %s", CHUNKS_FILE)
    chunks = load_chunks()
    log.info("Loaded %d chunks", len(chunks))

    log.info("Loading embedding model: %s", EMB_MODEL)
    model = SentenceTransformer(EMB_MODEL)

    log.info("Embedding %d chunks in batches of %d ...", len(chunks), BATCH_SIZE)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, batch_size=BATCH_SIZE, show_progress_bar=True).tolist()

    log.info("Connecting to Pinecone ...")
    pc    = Pinecone(api_key=PINECONE_API_KEY)
    index = get_or_create_index(pc)

    vectors = build_pinecone_vectors(chunks, embeddings)
    log.info("Upserting %d vectors into index '%s' ...", len(vectors), INDEX_NAME)
    upsert_in_batches(index, vectors, BATCH_SIZE)

    stats = index.describe_index_stats()
    log.info("Index stats: %s", stats)

    log.info("="*50)
    log.info("Embedding + indexing complete")
    log.info("  Vectors in Pinecone : %d", stats["total_vector_count"])
    log.info("="*50)

    # Run 3 test queries to validate retrieval
    test_query(index, model, "What projects have I done with Kafka?")
    test_query(index, model, "Summarize my experience with LLMs and multi-agent systems")
    test_query(index, model, "What did I build at Troy and Banks?")


if __name__ == "__main__":
    run()
