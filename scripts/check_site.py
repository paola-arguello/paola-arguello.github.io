#!/usr/bin/env python3
"""Checks that run on every pull request, before anything is rendered.

1. atlas/concepts.csv: every row has the same number of columns as the
   header, and every id appears once.
2. Every relative link and image in the .qmd source points to a file that
   exists. Links inside HTML comments and web links are skipped.

Run from the repository root: python scripts/check_site.py
Exits with status 1 if anything fails.
"""

import csv
import pathlib
import re
import sys

ATLAS = pathlib.Path("atlas/concepts.csv")
SKIP_DIRS = {"docs", "renv", ".quarto"}
LINK_RE = re.compile(r"\]\(([^)\s]+)")
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def atlas_problems(path):
    with open(path, encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    header, body = rows[0], rows[1:]
    problems = [
        f"{path}: row {n} has {len(row)} columns, expected {len(header)}"
        for n, row in enumerate(body, start=2)
        if len(row) != len(header)
    ]
    ids = [row[0] for row in body]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    problems += [f"{path}: id '{i}' appears more than once" for i in duplicates]
    return problems


def local_links(text):
    """Return relative link targets, without #anchors, outside HTML comments."""
    text = COMMENT_RE.sub("", text)
    targets = [m.group(1) for m in LINK_RE.finditer(text)]
    targets = [t.split("#")[0] for t in targets]
    return [t for t in targets if t and not t.startswith(("http", "mailto:"))]


def link_problems(root):
    problems = []
    for page in sorted(root.rglob("*.qmd")):
        if SKIP_DIRS & set(page.parts):
            continue
        for target in local_links(page.read_text(encoding="utf-8")):
            if not (page.parent / target).exists():
                problems.append(f"{page}: broken link to {target}")
    return problems


def main():
    problems = atlas_problems(ATLAS) + link_problems(pathlib.Path("."))
    for problem in problems:
        print(f"FAIL {problem}")
    if problems:
        return 1
    print("PASS atlas table and all local links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
