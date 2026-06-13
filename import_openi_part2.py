import requests
import json
import time
import os

BASE_URL = "https://openi.nlm.nih.gov/api/search"
IMG_BASE = "https://openi.nlm.nih.gov"
OUTPUT_DIR = "output"
RESULTS_PER_PAGE = 25
EXTRA_NEEDED = 51

CLASSES = [
    ("pneumonia", 578),
    ("pleural effusion", 4798),
    ("pneumothorax", 5099),
    ("cardiomegaly", 679),
    ("atelectasis", 752),
    ("normal chest", 6588),
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load existing
with open(f"{OUTPUT_DIR}/openi_data.json") as f:
    all_data = json.load(f)

def fetch_page(query, page):
    params = {"query": query, "coll": "cxr", "m": page, "n": RESULTS_PER_PAGE}
    for attempt in range(3):
        try:
            resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=60)
            return resp.json()
        except:
            time.sleep(5)
    return None

for query, _ in CLASSES:
    existing = len(all_data.get(query, []))
    needed = 100 - existing
    if needed <= 0:
        continue
    
    print(f"\n📥 {query} (need {needed} more)")
    page = 3  # Start from page 3
    
    while len(all_data[query]) < 100:
        print(f"  Page {page}...", end=" ")
        data = fetch_page(query, page)
        if not data or "list" not in data:
            print("No data")
            break
        
        for item in data["list"]:
            if len(all_data[query]) >= 100:
                break
            if item.get("impression") and item.get("imgLarge"):
                all_data[query].append({
                    "uid": item.get("uid"),
                    "diagnosis": item.get("impression"),
                    "findings": item.get("MeSH", {}).get("major", []),
                    "problems": item.get("Problems", ""),
                    "image_url": IMG_BASE + item["imgLarge"],
                })
        
        print(f"({len(all_data[query])}/100)")
        if len(data["list"]) < RESULTS_PER_PAGE:
            break
        page += 1
        time.sleep(3)

with open(f"{OUTPUT_DIR}/openi_data.json", "w") as f:
    json.dump(all_data, f, indent=2)

print("\n🎉 Done!")
for q, imgs in all_data.items():
    print(f"  {q}: {len(imgs)} images")
