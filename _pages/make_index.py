#!/usr/bin/env python3
import yaml
from pathlib import Path
import slugify

DATA_DIR = Path("_data")

def load_yaml(name):
    return yaml.safe_load((DATA_DIR / f"{name}.yml").read_text(encoding="utf-8"))


categories = load_yaml("categories")
reviews = load_yaml("reviews")
bottles = load_yaml("bottles")
producers = load_yaml("producers")
bottlers = load_yaml("bottlers")
posts = load_yaml("posts") if (DATA_DIR / "posts.yml").exists() else {}

# ------------------------------------------------------------
# 1. Reproduce category-class-country-region.html
# ------------------------------------------------------------

def resolve_cccr(review_id):
    r = reviews[review_id]
    bottle = bottles[r["bottle"]]
    producer = producers[bottle["production"]["producer"]]

    def inherit(field):
        # If producer has the field directly, use it
        if field in producer and producer[field]:
            return producer[field]

        # If producer is a line, inherit from its distillery
        if producer.get("kind") == "line":
            dist_id = producer.get("distillery")
            if dist_id and dist_id in producers:
                dist = producers[dist_id]
                return dist.get(field, "")

        # Otherwise return empty string
        return ""


    category = inherit("category")
    clazz = inherit("class")
    country = inherit("country")
    region = inherit("region")

    return category, clazz, country, region

# ------------------------------------------------------------
# 2. Reproduce review-string.html
# ------------------------------------------------------------

def review_string(review_id):
    r = reviews[review_id]
    bottle = bottles[r["bottle"]]

    producer_name = producers[bottle["production"]["producer"]]["name"]
    bottle_name = bottle["marketing"].get("name", "")
    age = bottle["maturation"].get("age")
    vintage = bottle["production"].get("vintage")
    abv = bottle["bottling"].get("abv")
    bottler = bottlers.get(bottle["bottling"]["bottler"])
    system = r["review"]["grade"]["system"]

    age_snippet = f"{age}yo" if age else "NAS"

    # Reproduce review-href.html
    post_slug = r["post"]
    post = next((p for p in posts if p["slug"] == post_slug), None)
    url = f"{post['url']}#{review_id}" if post else f"#{review_id}"

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

# ------------------------------------------------------------
# 3. Build review-index.html
# ------------------------------------------------------------

def generate_index():
    out = []
    out.append("<div class=\"review-index\">")

    for category in categories:
        cat_name = category["name"]
        out.append(f"<h2 id=\"{slugify.slugify(cat_name)}\">{cat_name}</h2>")

        for item in category["items"]:
            item_name = item["name"]
            out.append(f"<h3 id=\"{slugify.slugify(item_name)}\">{item_name}</h3>")

            # Nested region case
            if "items" in item:
                for subitem in item["items"]:
                    sub_name = subitem["name"]
                    out.append(f"<h4 id=\"{slugify.slugify(sub_name)}\">{sub_name}</h4>")

                    for review_id in reviews:
                        c, cl, country, region = resolve_cccr(review_id)
                        if (
                            cat_name == c and
                            item["type"] == "class" and
                            subitem["type"] == "region" and
                            item_name == cl and
                            sub_name == region
                        ):
                            out.append(review_string(review_id))

            # Non-nested case
            else:
                for review_id in reviews:
                    c, cl, country, region = resolve_cccr(review_id)

                    if cat_name == c and item["type"] == "class" and item_name == cl:
                        out.append(review_string(review_id))

                    elif cat_name == "World Whiskey" and item_name == country:
                        out.append(review_string(review_id))

    out.append("</div>")
    return "\n".join(out)

# ------------------------------------------------------------
# 4. Write output file
# ------------------------------------------------------------

OUTPUT = Path("review-index_NEW.html")
OUTPUT.write_text(generate_index(), encoding="utf-8")
print(f"Wrote {OUTPUT}")
