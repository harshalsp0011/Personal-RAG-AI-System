# Project Progress

## Phase 1 — Ingestion Pipeline
- [x] Created project folder structure (`src/`, `data/chunks/`, `db/`)
- [x] Created Python virtual environment (`venv/`)
- [x] Installed Phase 1 dependencies (`tiktoken`, `pyyaml`, `pymupdf`, `python-docx`)
- [x] Created `config.yaml` — central config for chunk size, paths, models, LLM settings
- [x] Created `requirements.txt` — all dependencies across all phases
- [x] Created `.env.example` — API key template
- [x] Created `.gitignore` — excludes venv, .env, db/, data/chunks/, pycache, DS_Store
- [x] Built `src/ingest_pipeline.py`
  - [x] Loaders for `.md`, `.txt`, `.pdf`, `.docx`
  - [x] Sentence-boundary-aware chunker (400 tokens, 50 overlap)
  - [x] Metadata tagging per chunk (source, chunk_index, ingested_at)
  - [x] Content-hash deduplication
  - [x] JSONL output to `data/chunks/chunks.jsonl`
- [x] Ran pipeline on `Personal Files/`
  - [x] `Experience.md` → 6 chunks
  - [x] `Project.md` → 9 chunks
  - [x] Total: **15 chunks** written to `data/chunks/chunks.jsonl`

---

## Phase 2 — Embedding + Vector Store
- [x] Switched vector store from Chroma → **Pinecone** (free serverless tier)
- [x] Updated `config.yaml` — Pinecone index config (aws/us-east-1, cosine, dim=384)
- [x] Updated `.env.example` — added `PINECONE_API_KEY`
- [x] Updated `.gitignore` — removed `db/` entry (no local vector store anymore)
- [x] Installed `sentence-transformers`, `pinecone`, `python-dotenv` into venv
- [x] Built `src/embed_and_index.py`
  - [x] Loads chunks from `chunks.jsonl`
  - [x] Embeds with `all-MiniLM-L6-v2` (local, free, 384-dim)
  - [x] Creates Pinecone serverless index if not exists
  - [x] Upserts vectors + metadata in batches
  - [x] Runs 3 test queries after indexing to validate retrieval
- [x] Created `.env` with `PINECONE_API_KEY` and `GROQ_API_KEY`
- [x] Ran `embed_and_index.py` — 15 vectors upserted into Pinecone index `personal-rag`
- [x] Validated retrieval with 3 test queries — semantic search returning correct results

---

## Phase 3 — RAG API
- [x] Installed `groq`, `fastapi`, `uvicorn` into venv
- [x] Built `src/rag_api.py` (FastAPI)
  - [x] `POST /ask` — embed query → retrieve top-5 from Pinecone → prompt → Groq LLM → answer + citations
  - [x] `POST /ingest` — add new text at runtime, embeds and upserts to Pinecone
  - [x] `GET /search` — raw chunk search with scores
  - [x] `GET /health` — status + vector count + model info
- [x] Connected to Groq API (Llama 3.1 8B — free, ~1s response time)
- [x] Tested with real questions:
  - "What did I build at Troy and Banks?" → correct grounded answer with citations
  - "What are my skills with Kafka and streaming?" → detailed answer citing Project.md

---

## Phase 4 — Interfaces
- [ ] Build `src/chat_ui.py` (Streamlit)
  - [ ] Chat input + answer display
  - [ ] Source citations (collapsible)
  - [ ] File uploader (triggers `/ingest`)
- [ ] (Optional) Telegram bot
- [ ] (Optional) CLI tool

---

## Production / Enhancements
- [ ] Docker setup
- [ ] Redis caching for repeated queries
- [ ] RAGAS evaluation with golden Q&A dataset
- [ ] Langfuse observability
- [ ] Deploy to Railway / Render

---

## Known Issues & Planned Improvements

### Retrieval Quality
- [ ] **Metadata filtering for company/employer names** — query "What did I build at Troy and Banks?" scored low (0.24) because the company name appears in few chunks. Fix: tag each chunk with `employer` metadata during ingestion and filter by it before vector search. This makes employer-specific queries much more precise.
- [ ] **Hybrid search (BM25 + vector)** — keyword-heavy queries like exact company/project names benefit from BM25 on top of semantic search. Pure vector search misses exact string matches.
