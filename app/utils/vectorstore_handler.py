import streamlit as st
import io
import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List

import pdfplumber
import docx
from sentence_transformers import SentenceTransformer

VECTOR_DIR = Path("app/vectorstore")
VECTOR_DIR.mkdir(exist_ok=True)

INDEX_PATH = VECTOR_DIR / "faiss.index"
METADATA_PATH = VECTOR_DIR / "metadata.pkl"

EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 output dimension
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


# Loaded once at module level — not reloaded on every Streamlit rerun
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def _embed(texts: List[str]) -> np.ndarray:
    """Embed a list of texts locally. Returns (N, 384) float32 array."""
    model = load_model()
    return model.encode(texts, show_progress_bar=False, normalize_embeddings=True).astype(np.float32)


def _extract_text(file_bytes: bytes, filename: str) -> str:
    ext = Path(filename).suffix.lower()

    if ext == ".pdf":
        text_parts = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts)

    elif ext in (".docx", ".doc"):
        doc = docx.Document(io.BytesIO(file_bytes))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    raise ValueError(f"Unsupported file type: {ext}")


def _chunk_text(text: str, filename: str) -> List[dict]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append({"text": chunk_text, "source": filename})
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def _load_store():
    if INDEX_PATH.exists() and METADATA_PATH.exists():
        index = faiss.read_index(str(INDEX_PATH))
        metadata = pickle.loads(METADATA_PATH.read_bytes())
    else:
        index = faiss.IndexFlatL2(EMBEDDING_DIM)
        metadata = []
    return index, metadata


def get_total_chunks():
    index, _ = _load_store()
    return index.ntotal


def vectorize_and_store(file_bytes: bytes, filename: str) -> int:
    """Extract → chunk → embed locally → save to FAISS. Returns chunks added."""
    text = _extract_text(file_bytes, filename)
    chunks = _chunk_text(text, filename)

    if not chunks:
        return 0

    embeddings = _embed([c["text"] for c in chunks])
    index, metadata = _load_store()

    index.add(embeddings)
    metadata.extend(chunks)

    faiss.write_index(index, str(INDEX_PATH))
    METADATA_PATH.write_bytes(pickle.dumps(metadata))

    return len(chunks)


def similarity_search(query: str, top_k: int = 5) -> List[dict]:
    """Return chunks whose cosine similarity confidence is greater than 80%."""

    index, metadata = _load_store()

    if index.ntotal == 0:
        return []

    query_vec = _embed([query])
    scores, indices = index.search(query_vec, top_k)

    results = []

    for i, idx in enumerate(indices[0]):
        if idx < len(metadata):

            similarity = float(scores[0][i])
            confidence = similarity * 100

            if confidence >= 80:
                results.append({
                    **metadata[idx],
                    "score": similarity,
                    "confidence": round(confidence, 2)
                })

    return results

def delete_chunks_by_filename(filename: str) -> int:
    """Remove all chunks belonging to a specific file. Returns number of chunks removed."""
    index, metadata = _load_store()

    if index.ntotal == 0:
        return 0

    # Find indices to KEEP (everything except the target file)
    keep_indices = [i for i, m in enumerate(metadata) if m["source"] != filename]
    removed_count = len(metadata) - len(keep_indices)

    if removed_count == 0:
        return 0

    if not keep_indices:
        # All chunks belong to this file — reset store entirely
        new_index = faiss.IndexFlatL2(EMBEDDING_DIM)
        new_metadata = []
    else:
        # Reconstruct index with only kept vectors
        # FAISS doesn't support deletion, so we rebuild from scratch
        all_vectors = np.zeros((index.ntotal, EMBEDDING_DIM), dtype=np.float32)
        for i in range(index.ntotal):
            all_vectors[i] = index.reconstruct(i)

        kept_vectors = all_vectors[keep_indices]
        new_index = faiss.IndexFlatL2(EMBEDDING_DIM)
        new_index.add(kept_vectors)
        new_metadata = [metadata[i] for i in keep_indices]

    faiss.write_index(new_index, str(INDEX_PATH))
    METADATA_PATH.write_bytes(pickle.dumps(new_metadata))

    return removed_count