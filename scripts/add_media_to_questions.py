#!/usr/bin/env python3
"""إضافة صور طبية حقيقية للأسئلة من مكتبة CXR + ECG"""

import json, os, random
from pathlib import Path

QUESTIONS_DIR = Path("../questions")
MEDIA_BASE = "https://raw.githubusercontent.com/almagrahimohned-collab/medtach-content/main"

# 🖼️ Media mapping: concept → image type
CONCEPT_MEDIA = {
    "ecg_interpretation": {
        "source": "ecg",
        "urls": [f"{MEDIA_BASE}/media/ecg/normal/normal_{i}.png" for i in range(1, 17)],
        "description": "12-Lead ECG - Interpret the rhythm and findings"
    },
    "imaging_interpretation": {
        "source": "cxr",
        "urls": [
            f"{MEDIA_BASE}/media/library/cxr/pneumonia/pneumonia_{i}.png" for i in range(1, 11)
        ] + [
            f"{MEDIA_BASE}/media/library/cxr/effusion/effusion_{i}.png" for i in range(1, 11)
        ] + [
            f"{MEDIA_BASE}/media/library/cxr/pneumothorax/pneumothorax_{i}.png" for i in range(1, 11)
        ] + [
            f"{MEDIA_BASE}/media/library/cxr/cardiomegaly/cardiomegaly_{i}.png" for i in range(1, 11)
        ],
        "description": "Chest X-Ray - Identify the radiological findings"
    },
    "diagnosis": {
        "source": "mixed",
        "urls": [
            f"{MEDIA_BASE}/media/ecg/abnormal/stemi_anterior_{i}.png" for i in range(1, 5)
        ] + [
            f"{MEDIA_BASE}/media/ecg/abnormal/afib_{i}.png" for i in range(1, 6)
        ] + [
            f"{MEDIA_BASE}/media/library/cxr/normal/normal_{i}.png" for i in range(1, 11)
        ],
        "description": "Clinical image - Use to guide your diagnosis"
    },
    "emergency_reasoning": {
        "source": "ecg_emergency",
        "urls": [
            f"{MEDIA_BASE}/media/ecg/abnormal/vtach_{i}.png" for i in range(1, 5)
        ] + [
            f"{MEDIA_BASE}/media/ecg/abnormal/stemi_anterior_{i}.png" for i in range(1, 5)
        ] + [
            f"{MEDIA_BASE}/media/ecg/abnormal/brugada_{i}.png" for i in range(1, 3)
        ],
        "description": "Emergency ECG - Identify the life-threatening rhythm"
    },
}

# 📁 تجهيز كل ملفات الأسئلة
updated = 0
for root, dirs, files in os.walk(QUESTIONS_DIR):
    for file in files:
        if file == "index.json" or not file.endswith(".json"):
            continue
        
        filepath = Path(root) / file
        
        try:
            with open(filepath) as f:
                questions = json.load(f)
            
            if not isinstance(questions, list):
                continue
            
            for q in questions:
                # Skip if already has media
                if q.get("media", {}).get("url"):
                    continue
                
                concept = q.get("concept", "")
                media_config = CONCEPT_MEDIA.get(concept)
                
                if media_config and media_config["urls"]:
                    random_url = random.choice(media_config["urls"])
                    q["media"] = {
                        "type": "image",
                        "url": random_url,
                        "description": media_config["description"]
                    }
                    updated += 1
            
            with open(filepath, "w") as f:
                json.dump(questions, f, indent=2)
                
        except Exception as e:
            print(f"  ❌ {file}: {e}")

print(f"\n✅ Added media to {updated} questions!")
print(f"📸 ECG: {sum(1 for c in CONCEPT_MEDIA.values() if c['source'].startswith('ecg'))} sources")
print(f"🩻 CXR: {sum(1 for c in CONCEPT_MEDIA.values() if c['source'] in ['cxr', 'mixed'])} sources")
