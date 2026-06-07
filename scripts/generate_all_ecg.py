import matplotlib.pyplot as plt
import numpy as np
import os

OUTPUT_DIR = "../media/ecg/abnormal"
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['lines.linewidth'] = 1.5

def draw_grid(ax):
    for i in range(0, 10):
        ax.axhline(y=i*0.5, color='#ffcccc', linewidth=0.3)
        ax.axhline(y=i*1.0, color='#ffaaaa', linewidth=0.5)
    for i in range(0, 20):
        ax.axvline(x=i*0.2, color='#ffcccc', linewidth=0.3)
        ax.axvline(x=i*1.0, color='#ffaaaa', linewidth=0.5)

def save_ecg(ax, filename, title):
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=100, bbox_inches='tight')
    plt.close()
    print(f"✅ {filename}")

# Pericarditis - diffuse ST elevation
fig, ax = plt.subplots(1, 1, figsize=(10, 4))
draw_grid(ax)
t = np.linspace(0, 5, 1000)
ecg = np.zeros_like(t)
for beat in range(6):
    t0 = beat / 1.2
    if t0 < 4.5:
        idx = (t >= t0) & (t < t0 + 0.8)
        rel_t = t[idx] - t0
        p_wave = 0.15 * np.exp(-((rel_t - 0.08) ** 2) / 0.001)
        qrs = 1.0 * np.exp(-((rel_t - 0.20) ** 2) / 0.0003)
        # Diffuse ST elevation + PR depression
        st_elev = 0.25 * (rel_t > 0.20) * (rel_t < 0.40)
        pr_dep = -0.08 * (rel_t > 0.05) * (rel_t < 0.15)
        t_wave = 0.3 * np.exp(-((rel_t - 0.42) ** 2) / 0.005)
        ecg[idx] = p_wave + qrs + st_elev + pr_dep + t_wave
ax.plot(t, ecg, 'k-', linewidth=2)
save_ecg(ax, "pericarditis.png", "Pericarditis - Diffuse ST Elevation + PR Depression")

# LVH
fig, ax = plt.subplots(1, 1, figsize=(10, 4))
draw_grid(ax)
t = np.linspace(0, 5, 1000)
ecg = np.zeros_like(t)
for beat in range(6):
    t0 = beat / 1.2
    if t0 < 4.5:
        idx = (t >= t0) & (t < t0 + 0.8)
        rel_t = t[idx] - t0
        p_wave = 0.2 * np.exp(-((rel_t - 0.08) ** 2) / 0.001)
        qrs = 1.8 * np.exp(-((rel_t - 0.20) ** 2) / 0.0003)
        qrs += -0.5 * np.exp(-((rel_t - 0.18) ** 2) / 0.0002)
        t_wave = -0.3 * np.exp(-((rel_t - 0.40) ** 2) / 0.004)
        ecg[idx] = p_wave + qrs + t_wave
ax.plot(t, ecg, 'k-', linewidth=2)
save_ecg(ax, "lvh.png", "Left Ventricular Hypertrophy - Strain Pattern")

# Hyperkalemia
fig, ax = plt.subplots(1, 1, figsize=(10, 4))
draw_grid(ax)
t = np.linspace(0, 5, 1000)
ecg = np.zeros_like(t)
for beat in range(6):
    t0 = beat / 1.2
    if t0 < 4.5:
        idx = (t >= t0) & (t < t0 + 0.8)
        rel_t = t[idx] - t0
        # Peaked T waves + wide QRS
        qrs = 0.8 * np.exp(-((rel_t - 0.22) ** 2) / 0.0006)
        t_wave = 1.0 * np.exp(-((rel_t - 0.38) ** 2) / 0.001)
        ecg[idx] = qrs + t_wave
ax.plot(t, ecg, 'k-', linewidth=2)
save_ecg(ax, "hyperkalemia.png", "Hyperkalemia - Peaked T Waves + Wide QRS")

# Long QT
fig, ax = plt.subplots(1, 1, figsize=(10, 4))
draw_grid(ax)
t = np.linspace(0, 5, 1000)
ecg = np.zeros_like(t)
for beat in range(5):
    t0 = beat / 0.9
    if t0 < 4.5:
        idx = (t >= t0) & (t < t0 + 1.0)
        rel_t = t[idx] - t0
        p_wave = 0.15 * np.exp(-((rel_t - 0.08) ** 2) / 0.001)
        qrs = 1.0 * np.exp(-((rel_t - 0.20) ** 2) / 0.0003)
        t_wave = 0.4 * np.exp(-((rel_t - 0.55) ** 2) / 0.008)
        ecg[idx] = p_wave + qrs + t_wave
ax.plot(t, ecg, 'k-', linewidth=2)
save_ecg(ax, "long_qt.png", "Long QT Syndrome - Prolonged QTc")

# WPW
fig, ax = plt.subplots(1, 1, figsize=(10, 4))
draw_grid(ax)
t = np.linspace(0, 5, 1000)
ecg = np.zeros_like(t)
for beat in range(6):
    t0 = beat / 1.2
    if t0 < 4.5:
        idx = (t >= t0) & (t < t0 + 0.8)
        rel_t = t[idx] - t0
        # Delta wave + short PR
        delta = 0.3 * (rel_t > 0.02) * (rel_t < 0.08)
        qrs = 1.5 * np.exp(-((rel_t - 0.15) ** 2) / 0.0005)
        t_wave = 0.3 * np.exp(-((rel_t - 0.40) ** 2) / 0.004)
        ecg[idx] = delta + qrs + t_wave
ax.plot(t, ecg, 'k-', linewidth=2)
save_ecg(ax, "wpw.png", "WPW Syndrome - Delta Wave + Short PR + Wide QRS")

# Brugada
fig, ax = plt.subplots(1, 1, figsize=(10, 4))
draw_grid(ax)
t = np.linspace(0, 5, 1000)
ecg = np.zeros_like(t)
for beat in range(6):
    t0 = beat / 1.2
    if t0 < 4.5:
        idx = (t >= t0) & (t < t0 + 0.8)
        rel_t = t[idx] - t0
        qrs = 1.0 * np.exp(-((rel_t - 0.15) ** 2) / 0.0003)
        # Coved ST elevation + T inversion
        st_coved = 0.5 * np.exp(-((rel_t - 0.25) ** 2) / 0.003) * (rel_t > 0.18)
        t_inv = -0.4 * np.exp(-((rel_t - 0.40) ** 2) / 0.004)
        ecg[idx] = qrs + st_coved + t_inv
ax.plot(t, ecg, 'k-', linewidth=2)
save_ecg(ax, "brugada.png", "Brugada Syndrome - Coved ST Elevation V1-V3")

print("\n🎉 All abnormal ECG images generated!")
