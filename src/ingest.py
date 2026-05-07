import hashlib
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from src.parsers import pdf_parser, md_parser, ics_parser

COLLECTION_NAME = "planner"
EMBED_MODEL = "all-MiniLM-L6-v2"


def ingest_all(data_dir: str, chroma_path: str) -> None:
    data = Path(data_dir)
    if not data.exists():
        print(f"Error: data directory '{data_dir}' not found.")
        print("Create it and add your documents, then re-run.")
        return

    print(f"Loading embedding model ({EMBED_MODEL})...")
    model = SentenceTransformer(EMBED_MODEL)

    print(f"Connecting to vector store at {chroma_path}...")
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_or_create_collection(
        COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    all_chunks: list[dict] = []

    # --- PDFs (syllabi) ---
    syllabus_files = list((data / "syllabi").glob("*.pdf"))
    for fpath in syllabus_files:
        chunks = pdf_parser.parse(str(fpath))
        all_chunks.extend(chunks)
        print(f"  {fpath.name:<40} → {len(chunks):>3} chunks")

    # --- Markdown / TXT (tasks) ---
    task_files = list((data / "tasks").glob("*.md")) + list((data / "tasks").glob("*.txt"))
    for fpath in task_files:
        chunks = md_parser.parse(str(fpath))
        all_chunks.extend(chunks)
        print(f"  {fpath.name:<40} → {len(chunks):>3} chunks")

    # --- ICS (calendars) ---
    cal_files = list((data / "calendars").glob("*.ics"))
    for fpath in cal_files:
        chunks = ics_parser.parse(str(fpath))
        all_chunks.extend(chunks)
        print(f"  {fpath.name:<40} → {len(chunks):>3} chunks")

    if not all_chunks:
        print("\nNo documents found. Add files to data/syllabi/, data/tasks/, data/calendars/")
        return

    print(f"\nEmbedding {len(all_chunks)} chunks...")
    texts = [c["text"] for c in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32).tolist()

    ids = [_stable_id(t) for t in texts]
    metadatas = [c["metadata"] for c in all_chunks]

    print("Upserting into vector store...")
    # Chroma has a max batch size; chunk the upsert if needed
    batch_size = 500
    for i in range(0, len(ids), batch_size):
        collection.upsert(
            ids=ids[i:i+batch_size],
            embeddings=embeddings[i:i+batch_size],
            documents=texts[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size],
        )

    print(f"\nDone. {len(all_chunks)} chunks stored in {chroma_path}.")
    _print_summary(all_chunks)


def _stable_id(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:24]


def _print_summary(chunks: list[dict]) -> None:
    by_type: dict[str, int] = {}
    dates = [c["metadata"]["due_date"] for c in chunks if c["metadata"].get("due_date")]

    for c in chunks:
        t = c["metadata"].get("type", "unknown")
        by_type[t] = by_type.get(t, 0) + 1

    print("\nKnowledge base summary:")
    for t, count in sorted(by_type.items()):
        print(f"  {t:<12}: {count} chunks")

    if dates:
        dates_sorted = sorted(dates)
        print(f"\n  Earliest due date : {dates_sorted[0]}")
        print(f"  Latest due date   : {dates_sorted[-1]}")
