import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Rectangle, Circle, Arc, FancyBboxPatch, Polygon, Wedge
import os
import random

OUTPUT_DIR = "../media/imaging_samples"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_img(fig, name):
    ax = fig.gca()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(os.path.join(OUTPUT_DIR, name), dpi=120, bbox_inches='tight', pad_inches=0.05, facecolor='black')
    plt.close(fig)
    print(f"✅ {name}")

# ==================== 1. CXR - Normal ====================
fig, ax = plt.subplots(1, 1, figsize=(7, 7), facecolor='black')
ax.set_facecolor('black')

# Spine
spine = Rectangle((0.48, 0.1), 0.04, 0.7, fill=True, facecolor='#2a2a2a')
ax.add_patch(spine)

# Ribs
for i in range(8):
    y = 0.78 - i * 0.08
    rib = Ellipse((0.5, y), 0.62, 0.015, fill=False, edgecolor='#3a3a3a', linewidth=1.2, angle=2 if i % 2 == 0 else -2)
    ax.add_patch(rib)

# Lungs
left_lung = Ellipse((0.34, 0.48), 0.22, 0.50, fill=True, facecolor='#1a1a24', edgecolor='#2a2a34', linewidth=1.5)
right_lung = Ellipse((0.66, 0.48), 0.24, 0.52, fill=True, facecolor='#1a1a24', edgecolor='#2a2a34', linewidth=1.5)
ax.add_patch(left_lung); ax.add_patch(right_lung)

# Heart
heart = Ellipse((0.47, 0.52), 0.10, 0.16, fill=True, facecolor='#3a3a3a', edgecolor='#4a4a4a', linewidth=1)
ax.add_patch(heart)

# Diaphragm
diaph = Arc((0.5, 0.15), 0.6, 0.15, angle=180, theta1=0, theta2=180, fill=False, edgecolor='#3a3a3a', linewidth=2)
ax.add_patch(diaph)

# Clavicles
for y in [0.82, 0.80]:
    Rectangle((0.15, y), 0.7, 0.006, fill=True, facecolor='#4a4a4a')
    ax.add_patch(Rectangle((0.15, y), 0.7, 0.006, fill=True, facecolor='#4a4a4a'))

# Labels
ax.text(0.5, 0.95, 'CXR PA - Normal', color='white', fontsize=12, fontweight='bold', ha='center')
ax.text(0.5, 0.05, 'Lungs clear | Heart size normal | No effusion', color='#888888', fontsize=8, ha='center')
save_img(fig, "cxr_normal.png")

# ==================== 2. CXR - Pneumonia ====================
fig, ax = plt.subplots(1, 1, figsize=(7, 7), facecolor='black')
ax.set_facecolor('black')

spine = Rectangle((0.48, 0.1), 0.04, 0.7, fill=True, facecolor='#2a2a2a')
ax.add_patch(spine)

for i in range(8):
    y = 0.78 - i * 0.08
    ax.add_patch(Ellipse((0.5, y), 0.62, 0.015, fill=False, edgecolor='#3a3a3a', linewidth=1.2))

right_lung = Ellipse((0.66, 0.48), 0.24, 0.52, fill=True, facecolor='#1a1a24', edgecolor='#2a2a34', linewidth=1.5)
ax.add_patch(right_lung)

# Left lung with pneumonia infiltrate
left_lung = Ellipse((0.34, 0.45), 0.22, 0.48, fill=True, facecolor='#1a1a24', edgecolor='#2a2a34', linewidth=1.5)
ax.add_patch(left_lung)

# Infiltrate
infiltrate = Ellipse((0.28, 0.42), 0.12, 0.15, fill=True, facecolor='#3a3a3a', edgecolor='#5a5a5a', linewidth=1, alpha=0.8)
ax.add_patch(infiltrate)
air_bronchogram = Rectangle((0.26, 0.44), 0.04, 0.02, fill=True, facecolor='#1a1a24')
ax.add_patch(air_bronchogram)

heart = Ellipse((0.47, 0.52), 0.10, 0.16, fill=True, facecolor='#3a3a3a', edgecolor='#4a4a4a', linewidth=1)
ax.add_patch(heart)

diaph = Arc((0.5, 0.15), 0.6, 0.15, angle=180, theta1=0, theta2=180, fill=False, edgecolor='#3a3a3a', linewidth=2)
ax.add_patch(diaph)

for y in [0.82, 0.80]:
    ax.add_patch(Rectangle((0.15, y), 0.7, 0.006, fill=True, facecolor='#4a4a4a'))

ax.text(0.5, 0.95, 'CXR PA - LLL Pneumonia', color='#ff6666', fontsize=12, fontweight='bold', ha='center')
ax.text(0.5, 0.05, 'Left lower lobe consolidation with air bronchograms', color='#888888', fontsize=8, ha='center')
save_img(fig, "cxr_pneumonia.png")

# ==================== 3. ULTRASOUND - Normal Abdomen ====================
fig, ax = plt.subplots(1, 1, figsize=(6, 6), facecolor='black')
ax.set_facecolor('black')

# US扇形
wedge = Wedge((0.5, 0.05), 0.85, 30, 150, fill=True, facecolor='#0a0a15', edgecolor='#2a2a3a', linewidth=2)
ax.add_patch(wedge)

# Liver texture (random dots)
np.random.seed(42)
for _ in range(300):
    r = random.uniform(0.1, 0.7)
    angle = random.uniform(35, 145)
    x = 0.5 + r * np.cos(np.radians(angle))
    y = 0.05 + r * np.sin(np.radians(angle))
    if 0.1 < x < 0.9 and 0.1 < y < 0.9:
        ax.plot(x, y, '.', color='#2a2a2a', markersize=random.uniform(0.5, 1.5))

# Portal vein
portal = Rectangle((0.35, 0.45), 0.08, 0.008, fill=True, facecolor='#0a0a15', edgecolor='#3a3a3a', linewidth=1)
ax.add_patch(portal)

# Diaphragm
diaph = Arc((0.5, 0.75), 0.6, 0.1, angle=0, theta1=200, theta2=340, fill=False, edgecolor='#4a4a4a', linewidth=1.5)
ax.add_patch(diaph)

ax.text(0.5, 0.95, 'US Abdomen - Normal Liver', color='white', fontsize=12, fontweight='bold', ha='center')
ax.text(0.5, 0.05, 'Homogeneous echotexture | No masses | Normal vessels', color='#888888', fontsize=8, ha='center')
save_img(fig, "us_abdomen_normal.png")

# ==================== 4. ULTRASOUND - Gallstones ====================
fig, ax = plt.subplots(1, 1, figsize=(6, 6), facecolor='black')
ax.set_facecolor('black')

wedge = Wedge((0.5, 0.05), 0.85, 30, 150, fill=True, facecolor='#0a0a15', edgecolor='#2a2a3a', linewidth=2)
ax.add_patch(wedge)

np.random.seed(42)
for _ in range(300):
    r = random.uniform(0.1, 0.7)
    angle = random.uniform(35, 145)
    x = 0.5 + r * np.cos(np.radians(angle))
    y = 0.05 + r * np.sin(np.radians(angle))
    if 0.1 < x < 0.9 and 0.1 < y < 0.9:
        ax.plot(x, y, '.', color='#2a2a2a', markersize=random.uniform(0.5, 1.5))

# Gallbladder
gb = Ellipse((0.55, 0.45), 0.06, 0.12, fill=True, facecolor='#0a0a15', edgecolor='#4a4a4a', linewidth=2)
ax.add_patch(gb)

# Stones
for sx, sy in [(0.53, 0.38), (0.56, 0.42), (0.54, 0.48)]:
    stone = Circle((sx, sy), 0.015, fill=True, facecolor='white', edgecolor='#cccccc', linewidth=1)
    ax.add_patch(stone)
    # Shadow
    shadow = Rectangle((sx-0.01, sy-0.06), 0.02, 0.05, fill=True, facecolor='#0a0a15', alpha=0.7)
    ax.add_patch(shadow)

ax.text(0.5, 0.95, 'US Gallbladder - Cholelithiasis', color='#ffaa00', fontsize=12, fontweight='bold', ha='center')
ax.text(0.5, 0.05, 'Multiple gallstones with posterior acoustic shadowing', color='#888888', fontsize=8, ha='center')
save_img(fig, "us_gallstones.png")

# ==================== 5. CT Head - Normal ====================
fig, ax = plt.subplots(1, 1, figsize=(6, 6), facecolor='black')
ax.set_facecolor('black')

# Skull
skull = Ellipse((0.5, 0.5), 0.35, 0.38, fill=True, facecolor='#1a1a1a', edgecolor='#3a3a3a', linewidth=3)
ax.add_patch(skull)

# Brain
brain = Ellipse((0.5, 0.5), 0.30, 0.33, fill=True, facecolor='#0d0d15', edgecolor='#2a2a2a', linewidth=2)
ax.add_patch(brain)

# Ventricles (butterfly)
vent_l = Ellipse((0.42, 0.48), 0.04, 0.06, fill=True, facecolor='#1a1a1a', edgecolor='#2a2a2a', linewidth=1)
vent_r = Ellipse((0.58, 0.48), 0.04, 0.06, fill=True, facecolor='#1a1a1a', edgecolor='#2a2a2a', linewidth=1)
ax.add_patch(vent_l); ax.add_patch(vent_r)

# 3rd ventricle
third = Rectangle((0.48, 0.47), 0.04, 0.015, fill=True, facecolor='#1a1a1a')
ax.add_patch(third)

# Sulci
for _ in range(20):
    x = random.uniform(0.25, 0.75)
    y = random.uniform(0.25, 0.75)
    if np.sqrt((x-0.5)**2 + (y-0.5)**2) < 0.28:
        ax.plot(x, y, '.', color='#1a1a1a', markersize=1)

ax.text(0.5, 0.95, 'CT Head - Normal', color='white', fontsize=12, fontweight='bold', ha='center')
ax.text(0.5, 0.05, 'No hemorrhage | Ventricles normal | Midline centered', color='#888888', fontsize=8, ha='center')
save_img(fig, "ct_head_normal.png")

# ==================== 6. CT Head - Hemorrhage ====================
fig, ax = plt.subplots(1, 1, figsize=(6, 6), facecolor='black')
ax.set_facecolor('black')

skull = Ellipse((0.5, 0.5), 0.35, 0.38, fill=True, facecolor='#1a1a1a', edgecolor='#3a3a3a', linewidth=3)
ax.add_patch(skull)

brain = Ellipse((0.5, 0.5), 0.30, 0.33, fill=True, facecolor='#0d0d15', edgecolor='#2a2a2a', linewidth=2)
ax.add_patch(brain)

# Hemorrhage (bright white)
hemorrhage = Ellipse((0.35, 0.52), 0.08, 0.06, fill=True, facecolor='white', edgecolor='#dddddd', linewidth=2)
ax.add_patch(hemorrhage)

# Mass effect
vent_l = Ellipse((0.44, 0.48), 0.03, 0.05, fill=True, facecolor='#1a1a1a', edgecolor='#2a2a2a', linewidth=1)
vent_r = Ellipse((0.58, 0.48), 0.04, 0.06, fill=True, facecolor='#1a1a1a', edgecolor='#2a2a2a', linewidth=1)
ax.add_patch(vent_l); ax.add_patch(vent_r)

# Midline shift arrow
ax.arrow(0.5, 0.4, 0.06, 0, head_width=0.015, head_length=0.01, fc='#ff4444', ec='#ff4444')

ax.text(0.5, 0.95, 'CT Head - ICH (Basal Ganglia)', color='#ff4444', fontsize=12, fontweight='bold', ha='center')
ax.text(0.5, 0.05, 'Right basal ganglia hemorrhage with midline shift', color='#888888', fontsize=8, ha='center')
save_img(fig, "ct_head_hemorrhage.png")

# ==================== 7. MRI Brain - Normal ====================
fig, ax = plt.subplots(1, 1, figsize=(6, 6), facecolor='black')
ax.set_facecolor('black')

skull = Ellipse((0.5, 0.5), 0.35, 0.38, fill=True, facecolor='#222222', edgecolor='#444444', linewidth=3)
ax.add_patch(skull)

brain = Ellipse((0.5, 0.5), 0.30, 0.33, fill=True, facecolor='#111122', edgecolor='#333344', linewidth=2)
ax.add_patch(brain)

# Gray/white matter differentiation
gm = Ellipse((0.5, 0.5), 0.28, 0.31, fill=True, facecolor='#1a1a2e', edgecolor='#2a2a3e', linewidth=1)
ax.add_patch(gm)

wm = Ellipse((0.5, 0.5), 0.20, 0.23, fill=True, facecolor='#252540', edgecolor='#353550', linewidth=1)
ax.add_patch(wm)

vent_l = Ellipse((0.43, 0.48), 0.03, 0.05, fill=True, facecolor='#111122', edgecolor='#222233', linewidth=1)
vent_r = Ellipse((0.57, 0.48), 0.03, 0.05, fill=True, facecolor='#111122', edgecolor='#222233', linewidth=1)
ax.add_patch(vent_l); ax.add_patch(vent_r)

ax.text(0.5, 0.95, 'MRI Brain - Normal (T2 FLAIR)', color='white', fontsize=12, fontweight='bold', ha='center')
ax.text(0.5, 0.05, 'No lesions | Ventricles normal | Gray-white preserved', color='#888888', fontsize=8, ha='center')
save_img(fig, "mri_brain_normal.png")

print("\n🎉 All 7 imaging samples generated!")
print(f"📁 Location: {OUTPUT_DIR}")
