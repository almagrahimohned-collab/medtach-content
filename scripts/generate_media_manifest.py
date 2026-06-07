#!/usr/bin/env python3
"""توليد manifest.json لكل الـ media library"""

import json, os
from pathlib import Path

LIBRARY_DIR = Path("../media/library")
MANIFEST_FILE = LIBRARY_DIR / "manifest.json"

def build_manifest():
    manifest = {}
    
    if not LIBRARY_DIR.exists():
        print("❌ Library directory not found")
        return
    
    for modality_dir in sorted(LIBRARY_DIR.iterdir()):
        if not modality_dir.is_dir():
            continue
        
        modality = modality_dir.name
        manifest[modality] = {}
        
        for pattern_dir in sorted(modality_dir.iterdir()):
            if not pattern_dir.is_dir():
                continue
            
            pattern = pattern_dir.name
            # جمع كل ملفات png
            images = sorted([
                f.name for f in pattern_dir.iterdir()
                if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.svg']
            ])
            
            if images:
                manifest[modality][pattern] = images
                print(f"  📸 {modality}/{pattern}: {len(images)} images")
    
    # حفظ
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    total_modalities = len(manifest)
    total_images = sum(
        len(images) 
        for modality in manifest.values() 
        for images in modality.values()
    )
    
    print(f"\n✅ Manifest generated!")
    print(f"📊 {total_modalities} modalities, {total_images} total images")
    print(f"📁 Saved to: {MANIFEST_FILE}")

if __name__ == "__main__":
    build_manifest()
