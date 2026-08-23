#!/usr/bin/env python3
import yaml
import pandas as pd
from pathlib import Path
from slugify import slugify

DATA_DIR = Path("_data")

def load_yaml(name):
    return yaml.safe_load((DATA_DIR / f"{name}.yml").read_text(encoding="utf-8"))


# Load Jekyll data
categories = load_yaml("categories")
reviews = load_yaml("reviews")
bottles = load_yaml("bottles")
producers = load_yaml("producers")
bottlers = load_yaml("bottlers")
posts = load_yaml("posts") if (DATA_DIR / "posts.yml").exists() else []

# --------------------------------------------------------------------
# 1. category-class-country-region.html
# --------------------------------------------------------------------

def resolve_cccr(review_id):
    r = reviews[review_id]
    bottle = bottles[r["bottle"]]
    producer = producers[bottle["production"]["producer"]]

    def inherit(field):
        if field in producer and producer[field]:
            return producer[field]
        if producer.get("kind") == "line":
            dist_id = producer.get("distillery")
            if dist_id and dist_id in producers:
                dist = producers[dist_id]
                return dist.get(field, "")
        return ""

    category = inherit("category")
    clazz = inherit("class")
    country = inherit("country")
    region = inherit("region")

    return category, clazz, country, region

# --------------------------------------------------------------------
# 2. review-href.html passthrough
# --------------------------------------------------------------------



def review_href(review_id):
    return (
        f"{{% assign _review_id = '{review_id}' %}}"
        f"{{%- include review-href.html id=_review_id -%}}"
    )


# --------------------------------------------------------------------
# 3. review-string.html
# --------------------------------------------------------------------

def display_producer_name(review_id):
    r = reviews[review_id]
    bottle = bottles[r["bottle"]]
    producer = producers[bottle["production"]["producer"]]

    name = producer["name"]

    if producer.get("kind") == "line":
        dist_name = distillery_name_of(review_id)
        if dist_name:
            return f"{dist_name}: {name}"

    return name


def review_string(review_id):
    r = reviews[review_id]
    bottle = bottles[r["bottle"]]
    producer_name = display_producer_name(review_id)
    #producer_name = producers[bottle["production"]["producer"]]["name"]
    bottle_name = bottle["marketing"].get("name", "")
    age = bottle["maturation"].get("age")
    vintage = bottle["production"].get("vintage")
    abv = bottle["bottling"].get("abv")
    bottler = bottlers.get(bottle["bottling"]["bottler"])
    system = r["review"]["grade"]["system"]

    age_snippet = f"{age}yo" if age else "NAS"

    url = review_href(review_id)
    html = f'<div><a href="{url}">'

    if producer_name:
        html += f"{producer_name} "
    if bottle_name:
        html += f"\"{bottle_name}\" "
    html += age_snippet
    if vintage:
        html += f" ({vintage})"
    if abv:
        html += f" {abv}%"
    if bottler:
        html += f" <em>{bottler['name']}</em>"
    html += "</a>"
    if system != "three-tier-2026":
        html += '<span style="color:LightGray;">[legacy]</span>'
    html += "</div>"

    return html

# --------------------------------------------------------------------
# Helpers for Pandas table
# --------------------------------------------------------------------



def producer_name_of(review_id):
    r = reviews[review_id]
    bottle = bottles[r["bottle"]]
    return producers[bottle["production"]["producer"]]["name"]

def distillery_name_of(review_id):
    r = reviews[review_id]
    bottle = bottles[r["bottle"]]
    producer = producers[bottle["production"]["producer"]]

    if producer.get("kind") == "distillery":
        return producer["name"]

    if producer.get("kind") == "line":
        dist_id = producer.get("distillery")
        if dist_id and dist_id in producers:
            return producers[dist_id]["name"]

    return None

def category_path_of(review_id):
    c, cl, country, region = resolve_cccr(review_id)

    # Find the category definition in categories.yml
    for cat in categories:
        if cat["name"] != c:
            continue

        # Loop through second-level items
        for item in cat["items"]:
            item_type = item["type"]
            item_name = item["name"]

            # Scotch/Irish/Eau-de-vie/Other: type = class
            if item_type == "class":
                if item_name == cl:
                    # If this class has regions
                    if "items" in item:
                        for sub in item["items"]:
                            if sub["type"] == "region" and sub["name"] == region:
                                return (c, cl, region)
                    # No region → class only
                    return (c, cl)

            # World Whiskey: type = country
            if item_type == "country":
                if item_name == country:
                    return (c, country)

    # Fallback (should not happen)
    return (c,)


# --------------------------------------------------------------------
# Build Pandas table
# --------------------------------------------------------------------

def build_table():
    rows = []
    for review_id in reviews:
        dist_name = distillery_name_of(review_id)
        age = bottles[reviews[review_id]["bottle"]]["maturation"].get("age")
        display = review_string(review_id)
        producer_name = producer_name_of(review_id)
        cat_path = category_path_of(review_id)

        rows.append({
            "review_id": review_id,
            "category_path": cat_path,
            "distillery": dist_name,
            "has_distillery": dist_name is not None,
            "age": age,
            "age_sort_key": (0, None) if age is None else (1, age),
            "producer_name": producer_name,
            "display": display,
        })

    return pd.DataFrame(rows)

# --------------------------------------------------------------------
# Sorting logic
# --------------------------------------------------------------------

def sort_reviews(df):
    return df.sort_values(
        by=[
            "has_distillery",
            "distillery",
            "age_sort_key",
            "display"
        ],
        ascending=[False, True, True, True]
    )

# --------------------------------------------------------------------
# Rendering with spacing between distilleries
# --------------------------------------------------------------------

def render_group(df):
    out = []
    last_producer = None
    for _, row in df.iterrows():
        current_producer = row["producer_name"]
        if last_producer is not None and current_producer != last_producer:
            out.append("<br>")
        out.append(row["display"])
        last_producer = current_producer
    return out


# --------------------------------------------------------------------
# 4. review-index.html (new Pandas-based version)
# --------------------------------------------------------------------

def generate_index():
    table = build_table()
    out = []
    out.append('<div class="review-index">')

    for category in categories:
        cat_name = category["name"]
        out.append(f'<h2 id="{slugify(cat_name)}">{cat_name}</h2>')

        for item in category["items"]:
            item_name = item["name"]
            out.append(f'<h3 id="{slugify(item_name)}">{item_name}</h3>')

            if "items" in item:
                for subitem in item["items"]:
                    sub_name = subitem["name"]
                    out.append(f'<h4 id="{slugify(sub_name)}">{sub_name}</h4>')

                    subset = table[
                        table["category_path"] == (cat_name, item_name, sub_name)
                    ]
                    sorted_subset = sort_reviews(subset)
                    out.extend(render_group(sorted_subset))

            else:
                subset = table[
                    table["category_path"] == (cat_name, item_name)
                ]
                sorted_subset = sort_reviews(subset)
                out.extend(render_group(sorted_subset))

    out.append("</div>")
    return "\n".join(out)

# --------------------------------------------------------------------
# 5. Write output file
# --------------------------------------------------------------------

OUTPUT = Path("review-index.html")
OUTPUT.write_text(generate_index(), encoding="utf-8")
print(f"Wrote {OUTPUT}")
