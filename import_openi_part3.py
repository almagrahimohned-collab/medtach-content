import requests, json, time, os

BASE_URL = "https://openi.nlm.nih.gov/api/search"
IMG_BASE = "https://openi.nlm.nih.gov"
OUTPUT_DIR = "output"
HEADERS = {"User-Agent": "Mozilla/5.0"}

CLASSES = ["pneumonia","pleural effusion","pneumothorax","cardiomegaly","atelectasis","normal chest"]

with open(f"{OUTPUT_DIR}/openi_data.json") as f:
    all_data = json.load(f)

def fetch_page(query, page):
    params = {"query": query, "coll": "cxr", "m": page, "n": 25}
    for _ in range(3):
        try:
            resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=60)
            return resp.json()
        except:
            time.sleep(5)
    return None

for query in CLASSES:
    while len(all_data[query]) < 100:
        page = (len(all_data[query]) // 25) + 1
        data = fetch_page(query, page)
        if not data or "list" not in data: break
        for item in data["list"]:
            if len(all_data[query]) >= 100: break
            if item.get("impression") and item.get("imgLarge"):
                all_data[query].append({
                    "uid": item.get("uid"),
                    "diagnosis": item.get("impression"),
                    "findings": item.get("MeSH",{}).get("major",[]),
                    "problems": item.get("Problems",""),
                    "image_url": IMG_BASE + item["imgLarge"],
                })
        print(f"  {query}: {len(all_data[query])}/100")
        time.sleep(3)

with open(f"{OUTPUT_DIR}/openi_data.json","w") as f:
    json.dump(all_data, f, indent=2)

print("\n🎉 Done!")
for q, imgs in all_data.items(): print(f"  {q}: {len(imgs)}")
