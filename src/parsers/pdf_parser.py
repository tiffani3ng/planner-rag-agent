import re
from pathlib import Path
import pypdf


def parse(file_path: str) -> list[dict]:
    path = Path(file_path)
    reader = pypdf.PdfReader(file_path)

    full_text = ""
    for page in reader.pages:
        text = page.extract_text() or ""
        full_text += text + "\n"

    chunks = _chunk_text(full_text, source=path.name)
    return chunks


def _chunk_text(text: str, source: str) -> list[dict]:
    lines = [l.rstrip() for l in text.split("\n")]

    chunks = []
    current_lines: list[str] = []

    def flush():
        chunk_text = " ".join(l for l in current_lines if l).strip()
        if len(chunk_text) > 30:
            due_date = _extract_date(chunk_text)
            priority = _extract_priority(chunk_text)
            course = _extract_course(chunk_text)
            chunks.append({
                "text": chunk_text,
                "metadata": {
                    "source": source,
                    "type": "syllabus",
                    "due_date": due_date,
                    "priority": priority,
                    "course": course,
                }
            })

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_lines:
                flush()
                current_lines = []
            continue

        # Start a new chunk on section headers or assignment lines
        if _is_chunk_start(stripped) and current_lines:
            flush()
            current_lines = [stripped]
        else:
            current_lines.append(stripped)

    if current_lines:
        flush()

    return chunks


def _is_chunk_start(line: str) -> bool:
    patterns = [
        r"^(Assignment|Homework|HW|Lab|Exam|Midterm|Final|Project|Quiz|Due|Week\s+\d)",
        r"^\d+[\.\)]\s+\w",
        r"^[-•*]\s+\w",
        r"^[A-Z][A-Z\s]{4,}:",   # ALL CAPS section headers
    ]
    return any(re.match(p, line, re.IGNORECASE) for p in patterns)


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
    if any(w in text_lower for w in ["exam", "final", "midterm"]):
        return "high"
    if any(w in text_lower for w in ["project", "paper", "report", "essay"]):
        return "medium"
    return "low"


def _extract_course(text: str) -> str:
    m = re.search(
        r"\b(MATH\s*\d+|FIN\s*\d+|CS\s*\d+|HPS\s*\d+)\b", text, re.IGNORECASE
    )
    return m.group() if m else ""
