import re
from pathlib import Path


def parse(file_path: str) -> list[dict]:
    path = Path(file_path)
    text = path.read_text(encoding="utf-8")
    return _chunk_text(text, source=path.name)


def _chunk_text(text: str, source: str) -> list[dict]:
    lines = text.split("\n")
    chunks = []
    current_lines: list[str] = []
    current_section = ""

    def flush():
        chunk_text = " ".join(l.strip() for l in current_lines if l.strip()).strip()
        # Strip leading bullet/number markers for cleaner text
        chunk_text = re.sub(r"^[-*•]\s+", "", chunk_text)
        chunk_text = re.sub(r"^\d+[\.\)]\s+", "", chunk_text)
        if len(chunk_text) > 20:
            due_date = _extract_date(chunk_text)
            priority = _extract_priority(chunk_text)
            chunks.append({
                "text": f"{current_section + ': ' if current_section else ''}{chunk_text}",
                "metadata": {
                    "source": source,
                    "type": "task",
                    "due_date": due_date,
                    "priority": priority,
                    "course": _extract_course(chunk_text + " " + current_section),
                }
            })

    for line in lines:
        stripped = line.strip()

        # Markdown headers become section context
        if re.match(r"^#{1,3}\s+", stripped):
            if current_lines:
                flush()
                current_lines = []
            current_section = re.sub(r"^#+\s+", "", stripped)
            continue

        # Blank lines delimit chunks
        if not stripped:
            if current_lines:
                flush()
                current_lines = []
            continue

        # Bullet or numbered list items each become their own chunk
        if re.match(r"^[-*•]\s+|^\d+[\.\)]\s+", stripped):
            if current_lines:
                flush()
                current_lines = []
            current_lines = [stripped]
        else:
            current_lines.append(stripped)

    if current_lines:
        flush()

    return chunks


def _extract_date(text: str) -> str:
    patterns = [
        r"\b\d{4}-\d{2}-\d{2}\b",
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{4}\b",
        r"\b\d{1,2}/\d{1,2}/\d{4}\b",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group()
    return ""


def _extract_priority(text: str) -> str:
    text_lower = text.lower()
    if re.search(r"\b(urgent|critical|high.priority|exam|final|midterm)\b", text_lower):
        return "high"
    if re.search(r"\b(medium|project|paper|essay|report|presentation)\b", text_lower):
        return "medium"
    return "low"


def _extract_course(text: str) -> str:
    m = re.search(
        r"\b(MATH\s*\d+|FIN\s*\d+|CS\s*\d+|HPS\s*\d+|"
        r"Linear Algebra|Portfolio|Software Dev|Philosophy|Science)\b",
        text, re.IGNORECASE,
    )
    return m.group() if m else ""
