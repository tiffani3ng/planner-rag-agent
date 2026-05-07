import re
from pathlib import Path
from datetime import datetime, date

from icalendar import Calendar


def parse(file_path: str) -> list[dict]:
    path = Path(file_path)
    raw = path.read_bytes()
    cal = Calendar.from_ical(raw)

    chunks = []
    for component in cal.walk():
        if component.name != "VEVENT":
            continue

        summary = str(component.get("SUMMARY", "Unnamed Event"))
        description = str(component.get("DESCRIPTION", ""))
        location = str(component.get("LOCATION", ""))

        dtstart = component.get("DTSTART")
        dtend = component.get("DTEND")

        start_dt = _to_datetime(dtstart.dt) if dtstart else None
        end_dt = _to_datetime(dtend.dt) if dtend else None

        date_str = start_dt.strftime("%Y-%m-%d") if start_dt else ""
        time_str = ""
        if start_dt and hasattr(start_dt, "hour"):
            end_str = end_dt.strftime("%I:%M %p") if end_dt else ""
            time_str = f"{start_dt.strftime('%I:%M %p')} – {end_str}".strip(" –")

        # Build human-readable chunk text
        parts = [summary]
        if date_str:
            parts.append(f"on {date_str}")
        if time_str:
            parts.append(f"from {time_str}")
        if location:
            parts.append(f"in {location}")
        if description and description != "None":
            parts.append(f"— {description.strip()}")

        text = " ".join(parts)

        # Determine type and priority
        event_type = _classify_event(summary)
        priority = _extract_priority(summary + " " + description)
        course = _extract_course(summary + " " + description)

        chunks.append({
            "text": text,
            "metadata": {
                "source": path.name,
                "type": event_type,
                "due_date": date_str,
                "priority": priority,
                "course": course,
            }
        })

    return chunks


def _to_datetime(dt_val) -> datetime | None:
    if isinstance(dt_val, datetime):
        return dt_val
    if isinstance(dt_val, date):
        return datetime(dt_val.year, dt_val.month, dt_val.day)
    return None


def _classify_event(summary: str) -> str:
    s = summary.lower()
    if any(w in s for w in ["exam", "midterm", "final", "quiz", "test"]):
        return "exam"
    if any(w in s for w in ["hw", "homework", "assignment", "lab", "project", "due", "paper", "essay"]):
        return "deadline"
    if any(w in s for w in ["gym", "workout", "exercise", "run"]):
        return "routine"
    if any(w in s for w in ["class", "lecture", "seminar", "section"]):
        return "class"
    return "event"


def _extract_priority(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["exam", "final", "midterm"]):
        return "high"
    if any(w in t for w in ["project", "paper", "essay", "report", "lab"]):
        return "medium"
    return "low"


def _extract_course(text: str) -> str:
    m = re.search(
        r"\b(MATH\s*\d+|FIN\s*\d+|CS\s*\d+|HPS\s*\d+)\b",
        text, re.IGNORECASE,
    )
    return m.group() if m else ""
