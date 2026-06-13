import requests
import json
import time
import os

BASE_URL = "https://openi.nlm.nih.gov/api/search"
IMG_BASE = "https://openi.nlm.nih.gov"
OUTPUT_DIR = "output"
RESULTS_PER_PAGE = 25
TARGET_PER_CLASS = 100

CLASSES = [
    ("pneumonia", 578),
    ("pleural effusion", 4798),
    ("pneumothorax", 5099),
    ("cardiomegaly", 679),
    ("atelectasis", 752),
    ("normal chest", 6588),
]

os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def fetch_one_page(query, page):
    params = {"query": query, "coll": "cxr", "m": page, "n": RESULTS_PER_PAGE}
    for attempt in range(3):
        try:
            resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=60)
            return resp.json()
        except Exception as e:
            print(f"    Retry {attempt+1}/3: {e}")
            time.sleep(5)
    return None

def fetch_images(query, target):
    collected = []
    page = 1
    
    while len(collected) < target:
        print(f"  Page {page}...", end=" ")
        data = fetch_one_page(query, page)
        
        if not data or "list" not in data:
            print("No data")
            break
        
        items = data["list"]
        for item in items:
            if not item.get("impression"):
                continue
            findings = item.get("MeSH", {}).get("major", [])
            image_path = item.get("imgLarge", "")
            if not image_path:
                continue
            
            collected.append({
                "uid": item.get("uid"),
                "diagnosis": item.get("impression"),
                "findings": findings,
                "problems": item.get("Problems", ""),
                "image_url": IMG_BASE + image_path,
            })
            if len(collected) >= target:
                break
        
        print(f"({len(collected)}/{target})")
        
        if len(items) < RESULTS_PER_PAGE:
            break
        
        page += 1
        time.sleep(3)  # Wait 3 seconds between pages
    
    return collected[:target]

def main():
    all_data = {}
    
    for query, _ in CLASSES:
        print(f"\n📥 {query}")
        images = fetch_images(query, TARGET_PER_CLASS)
        all_data[query] = images
        print(f"  ✅ {len(images)} images")
        time.sleep(5)  # Wait between categories
    
    output_file = os.path.join(OUTPUT_DIR, "openi_data.json")
    with open(output_file, "w") as f:
        json.dump(all_data, f, indent=2)
    
    print(f"\n🎉 Done! {output_file}")
    for q, imgs in all_data.items():
        print(f"  {q}: {len(imgs)}")

if __name__ == "__main__":
    main()
