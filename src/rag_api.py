"""
Phase 3 — RAG API
FastAPI app exposing /ask, /ingest, /search, /health endpoints.
"""

import os
import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime

import yaml
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# Config + secrets
# ---------------------------------------------------------------------------

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

with open(ROOT / "config.yaml") as f:
    CFG = yaml.safe_load(f)

VS           = CFG["vector_store"]
INDEX_NAME   = VS["index_name"]
NAMESPACE    = VS["namespace"]
DIMENSION    = VS["dimension"]
METRIC       = VS["metric"]
CLOUD        = VS["cloud"]
REGION       = VS["region"]

LLM_CFG      = CFG["llm"]
TOP_K        = CFG["retrieval"]["top_k"]
EMB_MODEL    = CFG["embedding"]["model"]

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY     = os.getenv("GROQ_API_KEY")

if not PINECONE_API_KEY:
    raise EnvironmentError("PINECONE_API_KEY not set in .env")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not set in .env")

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Startup — load models and connect to services
# ---------------------------------------------------------------------------

log.info("Loading embedding model: %s", EMB_MODEL)
embedder = SentenceTransformer(EMB_MODEL)

log.info("Connecting to Pinecone ...")
pc = Pinecone(api_key=PINECONE_API_KEY)

existing = [idx.name for idx in pc.list_indexes()]
if INDEX_NAME not in existing:
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric=METRIC,
        spec=ServerlessSpec(cloud=CLOUD, region=REGION),
    )
index = pc.Index(INDEX_NAME)

groq_client = Groq(api_key=GROQ_API_KEY)

log.info("RAG API ready.")

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Personal RAG AI",
    description="Ask questions grounded in Harshal's personal documents.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class AskRequest(BaseModel):
    question: str
    top_k: int = TOP_K

class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[dict]
    model_used: str

class IngestRequest(BaseModel):
    text: str
    source: str = "manual"

class IngestResponse(BaseModel):
    status: str
    chunk_id: str
    source: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = TOP_K

# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a personal AI assistant for Harshal Patil.
Answer questions ONLY using the provided context chunks.
If the answer is not in the context, say: "I don't have information about that in your documents."
Always mention which source document you are referencing.
Be concise and specific."""


def embed(text: str) -> list[float]:
    return embedder.encode([text])[0].tolist()


def retrieve(query: str, top_k: int) -> list[dict]:
    q_vec = embed(query)
    results = index.query(
        vector=q_vec,
        top_k=top_k,
        namespace=NAMESPACE,
        include_metadata=True,
    )
    chunks = []
    for match in results["matches"]:
        chunks.append({
            "score":   round(match["score"], 4),
            "source":  match["metadata"]["source"],
            "text":    match["metadata"]["text"],
            "chunk_index": match["metadata"]["chunk_index"],
        })
    return chunks


def build_context(chunks: list[dict]) -> str:
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(f"[Source {i}: {chunk['source']}]\n{chunk['text']}")
    return "\n\n---\n\n".join(parts)


def call_llm(question: str, context: str) -> str:
    user_message = f"Context:\n{context}\n\nQuestion: {question}"
    response = groq_client.chat.completions.create(
        model=LLM_CFG["model"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        temperature=LLM_CFG["temperature"],
        max_tokens=LLM_CFG["max_tokens"],
    )
    return response.choices[0].message.content.strip()

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    log.info("POST /ask  question='%s'", req.question)

    chunks  = retrieve(req.question, req.top_k)
    context = build_context(chunks)
    answer  = call_llm(req.question, context)

    sources = [{"source": c["source"], "score": c["score"], "excerpt": c["text"][:200]} for c in chunks]

    log.info("  → answered using %d chunks", len(chunks))
    return AskResponse(
        question=req.question,
        answer=answer,
        sources=sources,
        model_used=LLM_CFG["model"],
    )


@app.post("/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    log.info("POST /ingest  source='%s'", req.source)

    chunk_id  = hashlib.md5(req.text.encode()).hexdigest()
    vector    = embed(req.text)

    index.upsert(
        vectors=[{
            "id":     chunk_id,
            "values": vector,
            "metadata": {
                "source":      req.source,
                "chunk_index": 0,
                "tokens":      len(req.text.split()),
                "text":        req.text,
                "ingested_at": datetime.utcnow().isoformat(),
            }
        }],
        namespace=NAMESPACE,
    )

    log.info("  → upserted chunk %s", chunk_id)
    return IngestResponse(status="ok", chunk_id=chunk_id, source=req.source)


@app.get("/search")
def search(q: str, top_k: int = TOP_K):
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    log.info("GET /search  q='%s'", q)
    chunks = retrieve(q, top_k)
    return {"query": q, "results": chunks}


@app.get("/health")
def health():
    stats = index.describe_index_stats()
    vector_count = stats.get("total_vector_count", 0)
    return {
        "status":       "ok",
        "vector_count": vector_count,
        "index":        INDEX_NAME,
        "model":        EMB_MODEL,
        "llm":          LLM_CFG["model"],
    }
