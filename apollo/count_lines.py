# count_lines.py
# A script to count the number of lines of code in a single directory

from pathlib import Path
from collections import defaultdict

import os
import re
import typing as t

DEFAULT_EXTS: tuple = (
    ".py", ".c", ".cpp", ".h", ".hpp", ".java", ".js", ".ts",
    )

def iter_source_files(root: Path, exts: t.Iterable[str]) -> t.Iterable[Path]:
    exts = {e.lower() for e in exts}
    for path, _, files in os.walk(root):
        for file in files:
            if Path(file).suffix.lower() in exts:
                yield Path(path) / file

_comment_rx = re.compile(r"^\s*(#|//)")  # crude but works for most

def count_file_lines(path: Path, skip_blank: bool = False, skip_comments: bool = False) -> int:
    n: int = 0
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                if skip_blank and not line.strip():
                    continue
                if skip_comments and _comment_rx.match(line):
                    continue
                n += 1

    except Exception as e:
        print(f"⚠️  Could not read {path}: {e}")
    return n


def summarise(counts: dict[Path, int]) -> tuple[int, dict[str, int]]:
    grand = 0
    per_ext = defaultdict(int)
    for fp, n in counts.items():
        grand += n
        per_ext[fp.suffix.lower()] += n
    return grand, dict(per_ext)


def main(dir: str, skip_blank: bool, skip_comments: bool, exts: list = []) -> None:
    exts: t.Iterable = exts if exts else DEFAULT_EXTS

    per_file_counts: dict[Path, int] = {}

    for src in iter_source_files(dir, exts):
        n = count_file_lines(src, skip_blank, skip_comments)
        per_file_counts[src] = n
        print(f"{src}: {n}")

    grand, per_ext = summarise(per_file_counts)
    print("\n── Totals ─────────────────────────────────────────────")
    for ext, n in sorted(per_ext.items(), key=lambda kv: kv[0]):
        print(f"{ext}: {n}")
    print("───────────────────────────────────────────────────────")
    print(f"Total: {grand}")