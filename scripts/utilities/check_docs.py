"""Check repo docs: relative Markdown links resolve, and Mermaid files start with a valid keyword.

Usage: python scripts/utilities/check_docs.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
MERMAID_START = (
    "flowchart", "graph", "sequenceDiagram", "erDiagram", "stateDiagram-v2", "classDiagram",
)
SKIP_DIRS = {"node_modules", ".git", ".venv"}


def main() -> int:
    problems: list[str] = []
    for md in ROOT.rglob("*.md"):
        if SKIP_DIRS & set(md.parts):
            continue
        text = md.read_text(encoding="utf-8")
        in_fence = False
        for line in text.splitlines():
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for target in LINK.findall(line):
                if re.match(r"^(https?:|mailto:|#)", target):
                    continue
                path = (md.parent / target.split("#")[0]).resolve()
                if not path.exists():
                    problems.append(f"{md.relative_to(ROOT)}: broken link -> {target}")
    for mmd in (ROOT / "docs" / "diagrams").glob("*.mmd"):
        first = next((ln.strip() for ln in mmd.read_text().splitlines() if ln.strip()
                      and not ln.strip().startswith("%%")), "")
        if not first.startswith(MERMAID_START):
            problems.append(f"{mmd.name}: unexpected first line {first!r}")
    for p in problems:
        print(p)
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
