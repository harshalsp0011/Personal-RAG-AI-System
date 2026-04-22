"""
Phase 1 — Ingestion Pipeline
Reads documents from Personal Files/, chunks them, tags metadata, writes chunks.jsonl
"""

import os
import re
import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime

import yaml
import tiktoken

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

ROOT = Path(__file__).parent.parent
with open(ROOT / "config.yaml") as f:
    CFG = yaml.safe_load(f)

SOURCES_DIR  = ROOT / CFG["ingestion"]["sources_dir"]
OUTPUT_DIR   = ROOT / CFG["ingestion"]["output_dir"]
OUTPUT_FILE  = OUTPUT_DIR / CFG["ingestion"]["output_file"]
CHUNK_SIZE   = CFG["ingestion"]["chunk_size"]
CHUNK_OVERLAP= CFG["ingestion"]["chunk_overlap"]
MIN_LEN      = CFG["ingestion"]["min_chunk_length"]
EXTENSIONS   = CFG["ingestion"]["supported_extensions"]

TOKENIZER = tiktoken.get_encoding("cl100k_base")


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_pdf(path: Path) -> str:
    import fitz
    doc = fitz.open(str(path))
    return "\n".join(page.get_text() for page in doc)


def load_docx(path: Path) -> str:
    from docx import Document
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs)


LOADERS = {
    ".md":   load_markdown,
    ".txt":  load_txt,
    ".pdf":  load_pdf,
    ".docx": load_docx,
}


# ---------------------------------------------------------------------------
# Chunker
# ---------------------------------------------------------------------------

def split_into_sentences(text: str) -> list[str]:
    """Split on sentence boundaries — never cut mid-sentence."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def token_len(text: str) -> int:
    return len(TOKENIZER.encode(text))


def chunk_text(text: str, source_name: str) -> list[dict]:
    """
    Sliding-window chunker that respects sentence boundaries.
    Returns list of dicts with text + metadata.
    """
    sentences = split_into_sentences(text)
    chunks = []
    current_sentences: list[str] = []
    current_tokens = 0

    for sentence in sentences:
        s_tokens = token_len(sentence)

        # If a single sentence exceeds chunk size, hard-split it
        if s_tokens > CHUNK_SIZE:
            if current_sentences:
                chunks.append(" ".join(current_sentences))
                current_sentences = []
                current_tokens = 0
            # Hard split the long sentence by words
            words = sentence.split()
            buffer: list[str] = []
            buf_tokens = 0
            for word in words:
                w_tokens = token_len(word)
                if buf_tokens + w_tokens > CHUNK_SIZE and buffer:
                    chunks.append(" ".join(buffer))
                    # keep overlap words
                    overlap_words = buffer[-5:]
                    buffer = overlap_words + [word]
                    buf_tokens = token_len(" ".join(buffer))
                else:
                    buffer.append(word)
                    buf_tokens += w_tokens
            if buffer:
                chunks.append(" ".join(buffer))
            continue

        if current_tokens + s_tokens > CHUNK_SIZE and current_sentences:
            chunks.append(" ".join(current_sentences))
            # Overlap: keep last few sentences
            overlap: list[str] = []
            overlap_tokens = 0
            for s in reversed(current_sentences):
                t = token_len(s)
                if overlap_tokens + t > CHUNK_OVERLAP:
                    break
                overlap.insert(0, s)
                overlap_tokens += t
            current_sentences = overlap
            current_tokens = overlap_tokens

        current_sentences.append(sentence)
        current_tokens += s_tokens

    if current_sentences:
        chunks.append(" ".join(current_sentences))

    # Build metadata records
    records = []
    for i, chunk_text_val in enumerate(chunks):
        if len(chunk_text_val) < MIN_LEN:
            continue
        chunk_id = hashlib.md5(chunk_text_val.encode()).hexdigest()
        records.append({
            "id":       chunk_id,
            "source":   source_name,
            "chunk_index": i,
            "text":     chunk_text_val,
            "tokens":   token_len(chunk_text_val),
            "metadata": {
                "source":      source_name,
                "chunk_index": i,
                "ingested_at": datetime.utcnow().isoformat(),
            }
        })
    return records


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def ingest_file(path: Path) -> list[dict]:
    ext = path.suffix.lower()
    loader = LOADERS.get(ext)
    if loader is None:
        log.warning("Skipping unsupported file: %s", path.name)
        return []
    log.info("Loading  %s", path.name)
    text = loader(path)
    text = re.sub(r'\n{3,}', '\n\n', text)   # collapse excessive blank lines
    chunks = chunk_text(text, source_name=path.name)
    log.info("  → %d chunks", len(chunks))
    return chunks


def run_pipeline():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_chunks: list[dict] = []

    files = [
        p for p in SOURCES_DIR.rglob("*")
        if p.is_file() and p.suffix.lower() in EXTENSIONS
    ]

    if not files:
        log.warning("No supported files found in %s", SOURCES_DIR)
        return

    log.info("Found %d file(s) to ingest", len(files))

    seen_ids: set[str] = set()
    for file_path in files:
        chunks = ingest_file(file_path)
        for chunk in chunks:
            if chunk["id"] not in seen_ids:   # deduplicate by content hash
                seen_ids.add(chunk["id"])
                all_chunks.append(chunk)

    # Write JSONL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk) + "\n")

    log.info("="*50)
    log.info("Ingestion complete")
    log.info("  Files processed : %d", len(files))
    log.info("  Total chunks    : %d", len(all_chunks))
    log.info("  Output          : %s", OUTPUT_FILE)
    log.info("="*50)

    # Quick stats
    sources = {}
    for c in all_chunks:
        src = c["source"]
        sources[src] = sources.get(src, 0) + 1
    for src, count in sources.items():
        log.info("  %-40s  %d chunks", src, count)


if __name__ == "__main__":
    run_pipeline()
