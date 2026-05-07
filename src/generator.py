import os
import anthropic

from src.config import today as _today

# ── prompts ───────────────────────────────────────────────────────────────────

_SYSTEM_TEMPLATE = """You are a sharp, personalized scheduling assistant for a college student.
You help the user plan their time based on their actual tasks, deadlines, and calendar events.

Today's date is {today} ({weekday}).

Rules:
- Use ONLY information from the provided context. Do not invent tasks or deadlines.
- Always cite the source document in square brackets after each task you mention, e.g. [cs350_syllabus.pdf] or [software_dev_tasks.md].
- Be specific and actionable: suggest concrete time blocks, ordering, and durations.
- Keep answers concise (under 300 words unless the question requires more detail).
- Use plain language — no unnecessary jargon.
- When scheduling, account for priorities: exams/finals > major projects > homework > routines.
- Format your response with clear structure (numbered steps or bullet points where appropriate).
"""

USER_TEMPLATE = """Here is the relevant information from the student's documents:

{context}

---

Student's question: {query}

Provide a helpful, cited, actionable answer."""

_client: anthropic.Anthropic | None = None


# ── public API ────────────────────────────────────────────────────────────────

def generate_answer(query: str, chunks: list[dict]) -> str:
    client = _get_client()

    if not chunks:
        return (
            "I couldn't find any relevant tasks or events in your documents for that question.\n"
            "Make sure you've run 'ingest' and that your data files are populated."
        )

    today = _today()
    system_prompt = _SYSTEM_TEMPLATE.format(
        today=today.strftime("%B %d, %Y"),
        weekday=today.strftime("%A"),
    )
    context = _format_context(chunks)

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        thinking={"type": "adaptive"},
        system=system_prompt,
        messages=[
            {"role": "user", "content": USER_TEMPLATE.format(context=context, query=query)},
        ],
    )
    return next(b.text for b in response.content if b.type == "text")


# ── helpers ───────────────────────────────────────────────────────────────────

def _format_context(chunks: list[dict]) -> str:
    lines = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("source", "unknown")
        due = f" | due: {chunk['due_date']}" if chunk.get("due_date") else ""
        priority = f" | priority: {chunk['priority']}" if chunk.get("priority") else ""
        score = f" | relevance: {chunk.get('score', 0):.2f}"
        header = f"[{i}] [{source}{due}{priority}{score}]"
        lines.append(f"{header}\n{chunk['text']}")
    return "\n\n".join(lines)


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY not set. Add it to your .env file:\n"
                "  echo 'ANTHROPIC_API_KEY=sk-ant-...' >> .env"
            )
        _client = anthropic.Anthropic(api_key=api_key)
    return _client
