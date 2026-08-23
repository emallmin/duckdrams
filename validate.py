#!/usr/bin/env python3
import yaml
from pathlib import Path

DATA_DIR = Path("_data")

def load_yaml(name):
    return yaml.safe_load((DATA_DIR / f"{name}.yml").read_text())

reviews = load_yaml("reviews")

def validate_missing_posts():
    print("Reviews missing a 'post:' field or with empty post:")
    print("----------------------------------------------------")

    for review_id, review in reviews.items():
        post = review.get("post")
        if post is None or str(post).strip() == "":
            print(review_id)

if __name__ == "__main__":
    validate_missing_posts()
