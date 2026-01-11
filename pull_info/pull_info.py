#!/usr/bin/env python3
import os
import re
import yaml
from bs4 import BeautifulSoup

# bottle-key:
#   production:
#     vintage: #
#     producer: #
#   maturation:
#     age: #
#     cask: #
#   bottling:
#     bottler: #
#     batching: # single_cask, small_batch
#     abv: #
#     outturn: #
#     natural_color: #
#     unchillfiltered: #
#     bottling_date: #
#     size: 700
#   marketing:
#     series: #
#     name: #
#     released: #
#     rrp:
#       amount: #
#       currency: EUR   
#   meta:
#     whiskybase_id: #
#     image:
#       url: #
#       source: whiskybase





def parse_whiskybase_html(filename, wb_id):

    data = {
        wb_id: {
            "production" : {
                "vintage" : None,
                "producer" : None 
            },
            "maturation" : {
                "age" : None,
                "cask" : None
            },
            "bottling" : {
                "bottler": None,
                "batching": None,
                "abv" : None,
                "outturn": None,
                "natural_color": None,
                "unchillfiltered": None,
                "bottling_date": None,
                "size": 700
            },
            "marketing" : {
                "series" : None,
                "name" : None,
                "released" : None,
                "rrp": {
                    "amount" : None,
                    "currency" : "EUR"
                }       
            },
            "meta": {
                "whiskybase_id": int(wb_id),
                "image": {
                    "url": None,
                    "source": "whiskybase" }
            }
        }        
    }


    with open(filename, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find the main whisky description block
    desc_div = soup.find("div", class_="whisky-description")
    if not desc_div:
        print(f"Warning: whisky-description div not found in {filename}")
        return data

    dl = desc_div.find("dl")
    if not dl:
        print(f"Warning: <dl> not found in whisky-description in {filename}")
        return data

    for dt in dl.find_all("dt"):
        dd = dt.find_next_sibling("dd")
        if not dd:
            continue

        label = dt.get_text(strip=True)
        value = dd.get_text(" ", strip=True)

        # Map labels to your YAML schema
        if label == "Distillery":
            data[wb_id]["production"]["producer"] = value
        elif label == "Bottler":
            data[wb_id]["bottling"]["bottler"] = value.split("(")[0].strip()
        elif label == "Stated Age":
            m = re.search(r"(\d+)", value)
            if m:
                data[wb_id]["maturation"]["age"] = int(m.group(1))
        elif label == "Vintage":
            data[wb_id]["production"]["vintage"] = int(value) if value.isdigit() else (value + " # check!")
        elif label == "Strength":
            data[wb_id]["bottling"]["abv"] = float(value.replace("%", "").strip())
        elif label == "Cask Type":
            data[wb_id]["maturation"]["cask"] = value
        elif label == "Number of bottles":
            if value.isdigit():
                data[wb_id]["bottling"]["outturn"] = int(value)
        elif label == "Bottled":
            data[wb_id]["bottling"]["bottling_date"] = value
        elif label == "Size":
            data[wb_id]["bottling"]["size"] = value
        elif label == "Added on":
            data[wb_id]["marketing"]["released"] = value + " # check!"
        elif label == "Bottling series":
            data[wb_id]["marketing"]["series"] = value

    # Find NC / UCF / Single Cask info
    # These images are usually in a <dd> inside whisky-description
    icon_dd = dl.find_all("dd")[-1]  # the last <dd> usually has icons
    if icon_dd:
        for img in icon_dd.find_all("img"):
            title = img.get("title", "").lower()
            if "uncolored" in title:
                data[wb_id]["bottling"]["natural_color"] = True
            if "non-chill" in title or "non chill" in title:
                data[wb_id]["bottling"]["unchillfiltered"] = True
            if "single cask" in title:
                data[wb_id]["bottling"]["batching"] = "single_cask"
      

    # Find image_id
    image = soup.find("img", src=re.compile(r"-big\.jpg$"))
    if image:
        src = image["src"]
        m = re.search(r"/(\d+)-big\.jpg$", src)
        if m:
            image_id = m.group(1)
            
            # Construct static URL
            wb_id_str = str(wb_id)
            wb_parts = list(wb_id_str)
            if len(wb_parts) < 3:
                # pad with zeros if needed
                wb_parts = ["0"]*(3-len(wb_parts)) + wb_parts
            # first/second/rest
            first = wb_parts[0]
            second = wb_parts[1]
            rest = ''.join(wb_parts[2:])
            url = f"https://static.whiskybase.com/storage/whiskies/{first}/{second}/{rest}/{image_id}-big.jpg"
            data[wb_id]["meta"]["image"]["url"] = url

    return data

def main():
    # Collect all .html files in current folder
    files = [f for f in os.listdir(".") if f.endswith(".html")]
    all_data = {}

    for file in files:
        m = re.match(r"(\d+)\.html", file)
        if not m:
            continue
        wb_id = m.group(1)
        entry = parse_whiskybase_html(file, wb_id)
        all_data.update(entry)

    # Write YAML
    with open("out.yml", "w", encoding="utf-8") as f:
        yaml.dump(all_data, f, sort_keys=False, allow_unicode=True)

    print(f"Processed {len(all_data)} files. Output written to out.yml")

if __name__ == "__main__":
    main()
