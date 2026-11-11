#!/usr/bin/env python3
"""Turn per-posting keyword counts into a ranked keyword-gap report.

Usage:
    python3 scripts/aggregate.py references/keywords/<set>.json hits.txt resume.txt > keywords.csv

hits.txt has one line per job posting:
    <posting_id>|<word_count>|<theme_index>:<count>,<theme_index>:<count>,...
(This is the counter output from build_counter.py with the posting id in front.
A trailing "|<top phrases>" part is ignored.)

resume.txt is the résumé as plain text.

Output columns: Rank, Keyword, Postings using it, % of postings, Total mentions,
On résumé (count), Leverage.
Postings with fewer than 30 words are skipped; they are almost always closed
("Job not found") pages, so check them and drop them from the tracker.
"""
import csv
import json
import re
import sys

MIN_WORDS = 30


def leverage(pct: float, on_resume: int) -> str:
    if on_resume >= 2:
        return "Covered"
    if pct >= 40 and on_resume == 0:
        return "High – missing"
    if pct >= 40:
        return "Medium – underused"
    if pct >= 20 and on_resume == 0:
        return "Medium – missing"
    return "Low"


def main(keyword_file: str, hits_file: str, resume_file: str) -> None:
    themes = json.load(open(keyword_file, encoding="utf-8"))["themes"]
    resume = open(resume_file, encoding="utf-8").read().lower()

    docs, skipped = [], []
    for line in open(hits_file, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        parts = line.split("|")
        if len(parts) < 3:
            continue
        posting, words, hits = parts[0], parts[1], parts[2]
        if not words.isdigit() or int(words) < MIN_WORDS:
            skipped.append(posting)
            continue
        counts = {}
        for pair in filter(None, hits.split(",")):
            i, c = pair.split(":")
            counts[int(i)] = int(c)
        docs.append(counts)

    n = len(docs)
    if n == 0:
        sys.exit("No usable postings in hits file.")

    rows = []
    for i, theme in enumerate(themes):
        df = sum(1 for d in docs if i in d)
        total = sum(d.get(i, 0) for d in docs)
        on = len(re.findall(r"\b(?:" + theme["pattern"] + ")", resume))
        pct = 100 * df / n
        rows.append([theme["label"], df, round(pct), total, on, leverage(pct, on)])
    rows.sort(key=lambda r: (-r[1], -r[3]))

    out = csv.writer(sys.stdout)
    out.writerow(["Rank", "Keyword", f"Postings using it (of {n})", "% of postings",
                  "Total mentions", "On résumé (count)", "Leverage"])
    for rank, r in enumerate(rows, 1):
        out.writerow([rank, r[0], r[1], f"{r[2]}%", r[3], r[4], r[5]])
    if skipped:
        print(f"Skipped {len(skipped)} near-empty postings (probably closed): {', '.join(skipped)}",
              file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
