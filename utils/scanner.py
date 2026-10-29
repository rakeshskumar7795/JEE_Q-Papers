"""Finds the PDFs in papers/ and works out year, exam, paper, shift and type from the names."""
import re
from pathlib import Path

PAPERS_DIR = Path(__file__).resolve().parent.parent / "papers"
YEAR_RE = re.compile(r"(?<!\d)(20[0-2]\d)(?!\d)")
FIRST_YEAR, LAST_YEAR = 2007, 2025


def _clean_title(stem: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[_\-.]+", " ", stem)).strip()


def describe(path: Path) -> dict:
    rel = path.relative_to(PAPERS_DIR)
    haystack = " ".join(rel.parts)
    low = haystack.lower()

    years = YEAR_RE.findall(haystack)
    year = int(years[0]) if years else 0  # 0 = unknown

    if "advanced" in low or "adv" in re.split(r"[\s_\-./]+", low):
        exam = "JEE Advanced"
    elif "main" in low:
        exam = "JEE Main"
    elif "iit" in low:
        exam = "IIT-JEE"
    else:
        exam = "JEE"

    paper = ""
    m = re.search(r"paper[\s_\-]*([12])|(?<![a-z])p([12])(?!\d)", low)
    if m:
        paper = f"Paper {m.group(1) or m.group(2)}"

    shift = ""
    m = re.search(r"shift[\s_\-]*([12])", low)
    if m:
        shift = f"Shift {m.group(1)}"

    kind = "Solutions" if re.search(r"solution|answer|(?<![a-z])key(?![a-z])", low) else "Question Paper"

    return {
        "path": str(path),
        "file": rel.as_posix(),
        "name": path.name,
        "title": _clean_title(path.stem),
        "year": year,
        "exam": exam,
        "paper": paper,
        "shift": shift,
        "kind": kind,
        "size_mb": round(path.stat().st_size / (1024 * 1024), 2),
    }


def folder_stamp() -> float:
    """Changes when PDFs are added, removed or replaced, so cached results refresh."""
    if not PAPERS_DIR.exists():
        return 0.0
    files = [p for p in PAPERS_DIR.rglob("*") if p.suffix.lower() == ".pdf"]
    return sum(p.stat().st_mtime for p in files) + len(files)


def scan_papers() -> list[dict]:
    PAPERS_DIR.mkdir(exist_ok=True)
    files = [p for p in PAPERS_DIR.rglob("*") if p.is_file() and p.suffix.lower() == ".pdf"]
    papers = [describe(p) for p in files]
    papers.sort(key=lambda d: (-d["year"], d["exam"], d["paper"], d["shift"], d["title"]))
    return papers


def missing_years(papers: list[dict]) -> list[int]:
    have = {p["year"] for p in papers}
    return [y for y in range(FIRST_YEAR, LAST_YEAR + 1) if y not in have]
