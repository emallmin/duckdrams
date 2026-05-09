#!/usr/bin/env python3
import re
from pathlib import Path

INPUT_FILE = "input.txt"

def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[’'‘´]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s

def main():
    script_dir = Path(__file__).resolve().parent
    input_path = script_dir / INPUT_FILE
    outdir = script_dir  # write .md files in same folder as script

    for line in input_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue

        match = re.match(r'"(.*?)"\s+(\d{4}-\d{2}-\d{2})', line)
        if not match:
            print(f"Skipping malformed line: {line}")
            continue

        title, date = match.groups()
        slug = slugify(title)

        year, month, day = date.split("-")
        old_url = f"https://duckdrams.com/{year}/{month}/{day}/{slug}/"

        filename = f"{date}-{slug}.md"
        filepath = outdir / filename

        content = f"""---
layout: single
title: "{title}"
date: {date}
categories: Legacy
tags: null
header:
  overlay_image: https://files.emilmallmin.com/coming_soon.png
  overlay_filter: 0.5
  teaser: https://files.emilmallmin.com/coming_soon.png
---

This post will soon be ported from the old blog. [Link to the original post]({old_url})

"""

        filepath.write_text(content, encoding="utf-8")
        print(f"Wrote {filepath}")

if __name__ == "__main__":
    main()
