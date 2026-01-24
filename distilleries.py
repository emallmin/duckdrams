"""
Creates a <producers>.md file that displays all reviews 
"""

import yaml
from pathlib import Path

# Paths
DATA_FILE = Path("_data/producers.yml")
OUTPUT_DIR = Path("_pages/distilleries")

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load YAML
with DATA_FILE.open("r", encoding="utf-8") as f:
    producers = yaml.safe_load(f)

# Template for each page
TEMPLATE = """---
title: "{title}"
permalink: /distilleries/{id}/
layout: single
---
{{% include reviews-from-distillery.html id="{id}" %}}
"""

# Generate one file per producer
for producer_id, producer_data in producers.items():
    title = producer_data.get("name", producer_id.capitalize())
    content = TEMPLATE.format(title=title, id=producer_id)

    outfile = OUTPUT_DIR / f"{producer_id}.md"
    outfile.write_text(content, encoding="utf-8")

    print(f"Created {outfile}")
