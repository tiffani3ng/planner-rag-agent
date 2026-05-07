#!/usr/bin/env python3
"""Planner RAG Agent — your AI scheduling assistant."""

import shutil
import time
from pathlib import Path

import click
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "chroma_db"
DATA_DIR = "data"

DIVIDER = "─" * 64


@click.group()
def cli():
    """Planner RAG Agent — ask questions about your schedule and deadlines."""
    pass


# ── ingest ────────────────────────────────────────────────────────────────────

@cli.command()
@click.option(
    "--data-dir", default=DATA_DIR, show_default=True,
    help="Directory containing syllabi/, tasks/, and calendars/ sub-folders.",
)
def ingest(data_dir: str):
    """Parse and embed all documents into the local vector store."""
    from src.ingest import ingest_all

    click.echo(f"\nScanning {data_dir}/...")
    ingest_all(data_dir, CHROMA_PATH)


# ── ask ───────────────────────────────────────────────────────────────────────

@cli.command()
@click.argument("query")
@click.option("--top-k", default=5, show_default=True, help="Number of chunks to retrieve.")
@click.option("--verbose", is_flag=True, help="Show retrieved chunks before the answer.")
def ask(query: str, top_k: int, verbose: bool):
    """Ask a natural-language scheduling question.

    \b
    Examples:
      python -m src.cli ask "What should I work on this afternoon?"
      python -m src.cli ask "What's due this week?" --top-k 8
      python -m src.cli ask "Plan my study time before midterms" --verbose
    """
    from src.retriever import get_retriever
    from src.generator import generate_answer

    retriever = get_retriever(CHROMA_PATH)

    click.echo(f"\nRetrieving relevant tasks...", nl=False)
    t0 = time.perf_counter()
    chunks = retriever.retrieve(query, k=top_k)
    retrieve_time = time.perf_counter() - t0
    click.echo(f" {len(chunks)} results ({retrieve_time:.1f}s)")

    if not chunks:
        click.echo(
            "\nNo relevant content found. "
            "Run 'ingest' first, or try rephrasing your question."
        )
        return

    if verbose:
        click.echo(f"\n{DIVIDER}")
        click.echo("Retrieved chunks:")
        for i, c in enumerate(chunks, 1):
            due = f"  due: {c['due_date']}" if c["due_date"] else ""
            click.echo(f"\n  {i}. [{c['source']}]{due}  (score: {c['score']})")
            click.echo(f"     {c['text'][:120]}{'...' if len(c['text']) > 120 else ''}")
        click.echo(DIVIDER)

    click.echo("Generating answer...\n")
    t0 = time.perf_counter()

    try:
        answer = generate_answer(query, chunks)
    except Exception as e:
        click.echo(f"\nError generating answer: {e}", err=True)
        return

    gen_time = time.perf_counter() - t0
    total_time = retrieve_time + gen_time

    click.echo(DIVIDER)
    click.echo(answer)
    click.echo(DIVIDER)
    click.echo(f"Response time: {total_time:.1f}s  (retrieve: {retrieve_time:.1f}s  generate: {gen_time:.1f}s)")


# ── list ──────────────────────────────────────────────────────────────────────

@cli.command("list")
def list_docs():
    """Show a summary of everything in the knowledge base."""
    from src.retriever import get_retriever

    retriever = get_retriever(CHROMA_PATH)
    retriever.list_knowledge_base()


# ── clear ─────────────────────────────────────────────────────────────────────

@cli.command()
@click.option("--yes", is_flag=True, help="Skip confirmation prompt.")
def clear(yes: bool):
    """Delete the vector store. You will need to re-ingest documents."""
    path = Path(CHROMA_PATH)
    if not path.exists():
        click.echo("No vector store found — nothing to clear.")
        return

    if not yes:
        click.confirm(
            f"This will permanently delete '{CHROMA_PATH}/'. Continue?",
            abort=True,
        )

    shutil.rmtree(path)
    click.echo(f"Vector store '{CHROMA_PATH}/' deleted.")


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cli()
