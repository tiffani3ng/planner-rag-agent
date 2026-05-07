from __future__ import annotations

import re
from datetime import datetime, timedelta

import chromadb
from sentence_transformers import SentenceTransformer

from src.ingest import COLLECTION_NAME, EMBED_MODEL
from src.config import today as _config_today

_model: SentenceTransformer | None = None
_client: chromadb.PersistentClient | None = None
_chroma_path: str = ""


def get_retriever(chroma_path: str) -> "Retriever":
    return Retriever(chroma_path)


class Retriever:
    def __init__(self, chroma_path: str) -> None:
        global _model, _client, _chroma_path

        # Cache the model and client across calls within the same process
        if _model is None:
            _model = SentenceTransformer(EMBED_MODEL)
        if _client is None or _chroma_path != chroma_path:
            _client = chromadb.PersistentClient(path=chroma_path)
            _chroma_path = chroma_path

        self.model = _model
        self.client = _client
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        try:
            self.collection = self.client.get_collection(COLLECTION_NAME)
        except Exception:
            self.collection = None

    def retrieve(self, query: str, k: int = 5) -> list[dict]:
        if self.collection is None:
            print("No knowledge base found. Run 'ingest' first.")
            return []

        query_embedding = self.model.encode([query]).tolist()

        # Optionally expand k to allow post-filtering by date hints
        fetch_k = min(k * 3, 30)
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=fetch_k,
            include=["documents", "metadatas", "distances"],
        )

        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        chunks = []
        for doc, meta, dist in zip(docs, metas, distances):
            chunks.append({
                "text": doc,
                "source": meta.get("source", ""),
                "type": meta.get("type", ""),
                "due_date": meta.get("due_date", ""),
                "priority": meta.get("priority", ""),
                "course": meta.get("course", ""),
                "score": round(1 - dist, 3),  # cosine similarity
            })

        # Apply soft date filtering if the query mentions a time frame
        date_range = _parse_date_range(query)
        if date_range:
            # Pull task chunks directly by metadata and merge with semantic results
            # so deadline-specific bullets aren't crowded out by syllabus overview text.
            deadline_chunks = _fetch_deadline_chunks(self.collection, date_range)
            chunks = _merge_chunks(deadline_chunks, chunks, k)
        else:
            chunks = chunks[:k]

        return chunks

    def list_knowledge_base(self) -> None:
        if self.collection is None:
            print("No knowledge base found. Run 'ingest' first.")
            return

        count = self.collection.count()
        print(f"\nKnowledge base: {count} chunks total\n")

        # Pull all metadata to compute summary
        all_data = self.collection.get(include=["metadatas"])
        metas = all_data["metadatas"]

        by_type: dict[str, int] = {}
        by_source: dict[str, int] = {}
        dates = []

        for m in metas:
            t = m.get("type", "unknown")
            s = m.get("source", "unknown")
            d = m.get("due_date", "")
            by_type[t] = by_type.get(t, 0) + 1
            by_source[s] = by_source.get(s, 0) + 1
            if d:
                dates.append(d)

        print("By type:")
        for t, n in sorted(by_type.items()):
            print(f"  {t:<14}: {n}")

        print("\nBy source file:")
        for s, n in sorted(by_source.items()):
            print(f"  {s:<40}: {n}")

        if dates:
            print(f"\nEarliest due date: {min(dates)}")
            print(f"Latest due date  : {max(dates)}")


# ── Date-range extraction helpers ─────────────────────────────────────────────

def _parse_date_range(query: str) -> tuple[datetime, datetime] | None:
    q = query.lower()
    today = datetime.combine(_config_today(), datetime.min.time())

    if re.search(r"\btoday\b", q):
        return today, today + timedelta(days=1)
    if re.search(r"\btomorrow\b", q):
        return today + timedelta(days=1), today + timedelta(days=2)
    if re.search(r"\bthis week\b", q):
        return today, today + timedelta(days=8)  # inclusive of Friday (7 days ahead)
    if re.search(r"\bnext week\b", q):
        return today + timedelta(days=7), today + timedelta(days=14)
    if re.search(r"\bthis month\b", q):
        return today, today + timedelta(days=30)

    # "in N days/weeks"
    m = re.search(r"\bin\s+(\d+)\s+(day|week)", q)
    if m:
        n = int(m.group(1))
        unit = m.group(2)
        delta = timedelta(days=n) if unit == "day" else timedelta(weeks=n)
        return today, today + delta

    # Named day: "this friday", "next monday"
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for i, day in enumerate(days):
        if day in q:
            target = today + timedelta(days=(i - today.weekday()) % 7)
            return target, target + timedelta(days=1)

    return None


def _fetch_deadline_chunks(
    collection, date_range: tuple[datetime, datetime]
) -> list[dict]:
    """Fetch all task-type chunks directly and return those with due_date in range."""
    start, end = date_range
    try:
        result = collection.get(
            where={"type": "task"},
            include=["documents", "metadatas"],
        )
    except Exception:
        return []

    chunks = []
    for doc, meta in zip(result["documents"], result["metadatas"]):
        d = meta.get("due_date", "")
        if not d:
            continue
        try:
            dt = _parse_any_date(d)
            if dt and start <= dt < end:
                chunks.append({
                    "text": doc,
                    "source": meta.get("source", ""),
                    "type": meta.get("type", ""),
                    "due_date": d,
                    "priority": meta.get("priority", ""),
                    "course": meta.get("course", ""),
                    "score": 1.0,  # exact metadata match
                })
        except Exception:
            pass
    return chunks


def _merge_chunks(
    deadline_chunks: list[dict], semantic_chunks: list[dict], k: int
) -> list[dict]:
    """Deadline chunks go first; fill remaining slots from semantic results."""
    seen = {c["text"] for c in deadline_chunks}
    merged = list(deadline_chunks)
    for c in semantic_chunks:
        if c["text"] not in seen:
            merged.append(c)
            seen.add(c["text"])
    return merged[:k]


def _soft_date_filter(
    chunks: list[dict], date_range: tuple[datetime, datetime], k: int
) -> list[dict]:
    """Return up to k chunks, prioritising those whose due_date falls in range."""
    start, end = date_range

    in_range, out_of_range = [], []
    for c in chunks:
        d = c.get("due_date", "")
        if d:
            try:
                dt = _parse_any_date(d)
                if dt and start <= dt < end:
                    in_range.append(c)
                    continue
            except Exception:
                pass
        out_of_range.append(c)

    combined = in_range + out_of_range
    return combined[:k]


def _parse_any_date(s: str) -> datetime | None:
    formats = [
        "%Y-%m-%d",
        "%B %d, %Y",
        "%b %d, %Y",
        "%b. %d, %Y",
        "%m/%d/%Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(s.strip(), fmt)
        except ValueError:
            pass
    return None
