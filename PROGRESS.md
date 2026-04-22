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
- [ ] Install `sentence-transformers`, `chromadb`
- [ ] Build `src/embed_and_index.py`
- [ ] Load chunks from `chunks.jsonl`
- [ ] Embed with `all-MiniLM-L6-v2` (local, free)
- [ ] Store vectors + metadata in Chroma (`db/chroma/`)
- [ ] Run first semantic search query

---

## Phase 3 — RAG API
- [ ] Build `src/rag_api.py` (FastAPI)
- [ ] `POST /ask` — embed query → retrieve → prompt → LLM → answer + citations
- [ ] `POST /ingest` — add new docs at runtime
- [ ] `GET /search` — raw chunk search
- [ ] `GET /health` — status + vector count
- [ ] Connect to Groq API (Llama 3.1 8B — free)
- [ ] Test with real questions via curl / Postman

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
