"""
🫁 CXR Library Generator v2
- Synthetic procedural generation
- Metadata: image_source = "synthetic"
- Ready for future "real" images
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Rectangle, Arc, Circle, Wedge
import os, random, json
from datetime import datetime

OUTPUT = "../media/library/cxr"
DPI = 130

# 📋 Metadata for each image
def save_metadata(folder, filename, pattern, image_type="synthetic"):
    """حفظ metadata لكل صورة"""
    meta = {
        "image": filename,
        "pattern": pattern,
        "source": image_type,
        "generated": datetime.now().isoformat(),
        "modality": "cxr",
        "version": "2.0"
    }
    meta_path = os.path.join(OUTPUT, folder, f"{filename.replace('.png', '.json')}")
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)

def draw_base_cxr(ax):
    """الهيكل الأساسي لـ CXR"""
    ax.set_facecolor('black')
    ax.add_patch(Rectangle((0.48, 0.08), 0.04, 0.7, fill=True, facecolor='#222'))
    for i in range(9):
        y = 0.78 - i * 0.08
        ax.add_patch(Ellipse((0.5, y), 0.6, 0.012, fill=False, edgecolor='#333', linewidth=1))
    for y in [0.82, 0.80]:
        ax.add_patch(Rectangle((0.15, y), 0.7, 0.005, fill=True, facecolor='#444'))
    ax.add_patch(Arc((0.5, 0.12), 0.58, 0.12, angle=180, theta1=0, theta2=180, fill=False, edgecolor='#333', linewidth=2))

def add_lungs(ax):
    ax.add_patch(Ellipse((0.34, 0.48), 0.21, 0.48, fill=True, facecolor='#1a1a24', edgecolor='#2a2a34', linewidth=1.5))
    ax.add_patch(Ellipse((0.66, 0.48), 0.23, 0.50, fill=True, facecolor='#1a1a24', edgecolor='#2a2a34', linewidth=1.5))

def add_heart(ax):
    ax.add_patch(Ellipse((0.47, 0.52), 0.09, 0.15, fill=True, facecolor='#3a3a3a', edgecolor='#4a4a4a', linewidth=1))

def add_labels(ax, title, subtitle):
    ax.text(0.5, 0.96, title, color='white', fontsize=10, fontweight='bold', ha='center')
    ax.text(0.5, 0.03, subtitle, color='#777', fontsize=7, ha='center')

def save(fig, path):
    ax = fig.gca()
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect('equal'); ax.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(path, dpi=DPI, bbox_inches='tight', pad_inches=0.05, facecolor='black')
    plt.close(fig)

# ============ NORMAL (8 images) ============
print("🫁 Normal CXR...")
for i in range(8):
    fig, ax = plt.subplots(1, 1, figsize=(7, 7))
    draw_base_cxr(ax); add_lungs(ax); add_heart(ax)
    add_labels(ax, "CXR PA - Normal", "Clear lungs | Normal heart size")
    filename = f"normal_{i+1}.png"
    save(fig, os.path.join(OUTPUT, "normal", filename))
    save_metadata("normal", filename, "normal")
    print(f"  ✅ {filename}")

# ============ PNEUMONIA (8 images) ============
print("🫁 Pneumonia CXR...")
for i in range(8):
    fig, ax = plt.subplots(1, 1, figsize=(7, 7))
    draw_base_cxr(ax)
    ax.add_patch(Ellipse((0.66, 0.48), 0.23, 0.50, fill=True, facecolor='#1a1a24', edgecolor='#2a2a34', linewidth=1.5))
    ax.add_patch(Ellipse((0.34, 0.48), 0.21, 0.48, fill=True, facecolor='#1a1a24', edgecolor='#2a2a34', linewidth=1.5))
    
    locs = [(0.30, 0.40, 0.10, 0.14), (0.28, 0.55, 0.11, 0.12), (0.34, 0.35, 0.12, 0.16), (0.62, 0.42, 0.10, 0.15),
            (0.32, 0.48, 0.09, 0.13), (0.65, 0.55, 0.10, 0.12), (0.30, 0.50, 0.11, 0.10), (0.64, 0.38, 0.09, 0.16)]
    x, y, w, h = locs[i]
    ax.add_patch(Ellipse((x, y), w, h, fill=True, facecolor='#4a4a4a', edgecolor='#6a6a6a', linewidth=1.5, alpha=0.9))
    ax.add_patch(Rectangle((x-0.02, y+0.01), 0.03, 0.015, fill=True, facecolor='#1a1a24'))
    
    add_heart(ax)
    add_labels(ax, "CXR PA - Pneumonia", "Lobar consolidation with air bronchograms")
    filename = f"pneumonia_{i+1}.png"
    save(fig, os.path.join(OUTPUT, "pneumonia", filename))
    save_metadata("pneumonia", filename, "pneumonia")
    print(f"  ✅ {filename}")

# ============ EFFUSION (5 images) ============
print("🫁 Effusion CXR...")
for i in range(5):
    fig, ax = plt.subplots(1, 1, figsize=(7, 7))
    draw_base_cxr(ax); add_lungs(ax); add_heart(ax)
    ax.add_patch(Arc((0.5, 0.18), 0.55, 0.15 + i*0.02, angle=180, theta1=0, theta2=180, fill=False, edgecolor='#666', linewidth=3))
    ax.add_patch(Wedge((0.5, 0.2), 0.3, 0, 180, fill=True, facecolor='#3a3a3a', alpha=0.6))
    add_labels(ax, "CXR PA - Pleural Effusion", "Right pleural effusion with meniscus sign")
    filename = f"effusion_{i+1}.png"
    save(fig, os.path.join(OUTPUT, "effusion", filename))
    save_metadata("effusion", filename, "effusion")
    print(f"  ✅ {filename}")

# ============ PNEUMOTHORAX (5 images) ============
print("🫁 Pneumothorax CXR...")
for i in range(5):
    fig, ax = plt.subplots(1, 1, figsize=(7, 7))
    draw_base_cxr(ax); add_heart(ax)
    collapse = [0.12, 0.15, 0.10, 0.14, 0.11]
    ax.add_patch(Ellipse((0.66, 0.48), 0.23, 0.50, fill=True, facecolor='#1a1a24', edgecolor='#2a2a34', linewidth=1.5))
    ax.add_patch(Ellipse((0.30, 0.48), collapse[i], 0.35, fill=True, facecolor='#1a1a24', edgecolor='#2a2a34', linewidth=1.5))
    px = 0.18 + i*0.015
    ax.plot([px, px], [0.15, 0.78], color='#555', linewidth=1.5)
    ax.add_patch(Rectangle((px-0.1, 0.15), 0.1, 0.63, fill=True, facecolor='black', alpha=0.5))
    add_labels(ax, "CXR PA - Pneumothorax", "Left-sided pneumothorax with lung collapse")
    filename = f"pneumothorax_{i+1}.png"
    save(fig, os.path.join(OUTPUT, "pneumothorax", filename))
    save_metadata("pneumothorax", filename, "pneumothorax")
    print(f"  ✅ {filename}")

# ============ CARDIOMEGALY (4 images) ============
print("🫁 Cardiomegaly CXR...")
for i in range(4):
    fig, ax = plt.subplots(1, 1, figsize=(7, 7))
    draw_base_cxr(ax); add_lungs(ax)
    size = 0.10 + i*0.01
    ax.add_patch(Ellipse((0.47, 0.52), size, 0.17, fill=True, facecolor='#4a4a4a', edgecolor='#5a5a5a', linewidth=1))
    add_labels(ax, "CXR PA - Cardiomegaly", "Enlarged cardiac silhouette | CTR >0.5")
    filename = f"cardiomegaly_{i+1}.png"
    save(fig, os.path.join(OUTPUT, "cardiomegaly", filename))
    save_metadata("cardiomegaly", filename, "cardiomegaly")
    print(f"  ✅ {filename}")

# 📊 Summary
total = sum(len([f for f in os.listdir(os.path.join(OUTPUT, d)) if f.endswith('.png')]) for d in os.listdir(OUTPUT) if os.path.isdir(os.path.join(OUTPUT, d)))
print(f"\n🎉 CXR Library Complete: {total} images + metadata")
print(f"📁 Location: {OUTPUT}")
print(f"📋 image_source: synthetic (ready for 'real' upgrade)")
