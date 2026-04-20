# Personal RAG AI System — Architecture

## Full System Architecture

```mermaid
flowchart TD
    subgraph SOURCES["📂 DATA SOURCES"]
        S1[PDF / DOCX / TXT / MD]
        S2[Gmail API]
        S3[Notion API]
        S4[GitHub API]
        S5[CSV / Structured Data]
    end

    subgraph INGEST["⚙️ PHASE 1 — INGESTION PIPELINE (ingest_pipeline.py)"]
        P1[Document Loaders\nLangChain / PyMuPDF / python-docx]
        P2[Text Cleaner\nRemove noise, normalize whitespace]
        P3[Chunker\n400 tokens, 50-token overlap\nPreserve sentence boundaries]
        P4[Metadata Tagger\nsource, page, date, section, chunk_id = hash]
        P5[(JSONL Output\n id, source, text, metadata )]
    end

    subgraph EMBED["🔢 PHASE 2 — EMBEDDING + INDEX (embed_and_index.py)"]
        E1[Embedding Model\nall-MiniLM-L6-v2 local\nOR OpenAI ada-002 API]
        E2[(Vector Store\nChroma local\nOR Pinecone cloud)]
        E3[Metadata Store\nstored alongside vectors]
    end

    subgraph API["🧠 PHASE 3 — RAG API (rag_api.py — FastAPI)"]
        A1[POST /ask\nquestion, top_k=5]
        A2[Embed Query\nsame model as index time]
        A3[Vector Search\ncosine similarity → top-5 chunks]
        A4[Prompt Builder\nSystem prompt + chunks + question]
        A5[LLM\nGroq Llama 3.1 8B free\nOR OpenAI GPT-3.5/4o\nOR Ollama local]
        A6[Response\nanswer + source citations + confidence]
        A7[POST /ingest\nadd new docs at runtime]
        A8[GET /search\nraw chunk search]
        A9[GET /health\nstatus + vector count]
    end

    subgraph UI["🖥️ PHASE 4 — INTERFACES"]
        U1[Streamlit Chat UI\nQ&A + file upload + citations]
        U2[Telegram Bot\npython-telegram-bot]
        U3[Slack Bot\nSlack Webhooks]
        U4[CLI Tool\nrag-ask 'your question']
    end

    subgraph OPS["🔧 PRODUCTION / OPS"]
        O1[Redis Cache\nrepeated queries]
        O2[Docker\ncontainerized stack]
        O3[Railway / Render\nfree cloud hosting]
        O4[Langfuse / LangSmith\nobservability + query logs]
        O5[GitHub Actions\nCI/CD auto-redeploy]
        O6[RAGAS Evaluation\nfaithfulness, relevancy, precision]
    end

    %% Data flow: Sources → Ingestion
    S1 & S2 & S3 & S4 & S5 --> P1
    P1 --> P2 --> P3 --> P4 --> P5

    %% Ingestion → Embedding
    P5 --> E1 --> E2
    P4 --> E3
    E2 <--> E3

    %% Query flow: User → API → Vector Store → LLM → Response
    U1 & U2 & U3 & U4 -->|HTTP POST /ask| A1
    A1 --> A2 --> A3
    A3 <-->|similarity search| E2
    A3 --> A4 --> A5 --> A6
    A6 -->|JSON response| U1 & U2 & U3 & U4

    %% Other endpoints
    A1 --- A7 & A8 & A9

    %% Runtime ingestion
    A7 --> E1

    %% Ops wiring
    A1 <--> O1
    A5 --> O4
    A1 --> O4
    O6 -->|test suite| A1
    O5 --> O3
    O2 --> O3
```

---

## Data Flow — Step by Step

```
USER QUESTION
     │
     ▼
[Interface: Streamlit / Telegram / Slack / CLI]
     │  HTTP POST /ask { question }
     ▼
[FastAPI — /ask endpoint]
     │
     ├─1─▶ Embed question  →  [Embedding Model]  →  query_vector
     │
     ├─2─▶ Search vector store  →  [Chroma / Pinecone]  →  top-5 chunks
     │                                      ▲
     │                              (indexed at ingest time)
     │
     ├─3─▶ Build prompt:
     │        System: "Answer ONLY from context. Cite sources."
     │        Context: chunk1 + chunk2 + chunk3 + chunk4 + chunk5
     │        Question: user's question
     │
     ├─4─▶ Call LLM  →  [Groq / OpenAI / Ollama]  →  answer text
     │
     └─5─▶ Return JSON:
              { answer, sources: [{file, page, excerpt}], confidence }
```

---

## Component Responsibility Map

| Layer | Component | Responsibility |
|---|---|---|
| Sources | Gmail, Notion, PDF, GitHub | Raw data |
| Ingestion | `ingest_pipeline.py` | Parse → chunk → tag → JSONL |
| Embedding | `embed_and_index.py` | Text → vectors → vector DB |
| Vector DB | Chroma / Pinecone | Store & search vectors |
| API | `rag_api.py` | Orchestrate retrieve → generate |
| LLM | Groq / OpenAI / Ollama | Generate grounded answer |
| Interfaces | Streamlit / Telegram / CLI | User-facing interaction |
| Ops | Docker / Redis / Langfuse | Infra, caching, observability |

---

## Deployment Architecture

```
                        ┌─────────────────────────────┐
                        │        Railway / Render       │
                        │   ┌──────────────────────┐   │
                        │   │   FastAPI (rag_api)   │   │
                        │   │   + Redis cache       │   │
                        │   └──────────┬───────────┘   │
                        │              │                │
                        │   ┌──────────▼───────────┐   │
                        │   │   Pinecone (cloud)    │   │
                        │   │   Vector Store        │   │
                        │   └──────────────────────┘   │
                        └─────────────────────────────┘
                                       ▲
              ┌────────────────────────┼────────────────────────┐
              │                        │                        │
   ┌──────────▼──────┐    ┌────────────▼───────┐   ┌──────────▼──────┐
   │ Streamlit Cloud  │    │  Telegram Bot       │   │  Slack Bot      │
   │ (Chat UI)        │    │  (Mobile access)    │   │  (Team access)  │
   └──────────────────┘    └────────────────────┘   └─────────────────┘
```
