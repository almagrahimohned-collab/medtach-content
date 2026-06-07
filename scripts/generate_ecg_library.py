import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import random

# إعدادات الصورة - أكبر وأوضح
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['lines.linewidth'] = 2.0
plt.rcParams['font.size'] = 9
plt.rcParams['font.family'] = 'sans-serif'

OUTPUT_DIR = "../media/ecg"
DPI = 150  # أعلى دقة

def save_ecg(fig, filepath, title=""):
    """حفظ الصورة بجودة عالية بدون مسافات زائدة"""
    ax = fig.gca()
    ax.set_title(title, fontsize=11, fontweight='bold', pad=6)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.tight_layout(pad=0.5)
    plt.savefig(filepath, dpi=DPI, bbox_inches='tight', pad_inches=0.1, facecolor='white')
    plt.close(fig)
    print(f"  ✅ {os.path.basename(filepath)}")

def draw_grid(ax, rows=8, cols=20):
    """رسم شبكة خفيفة"""
    for i in range(rows * 2):
        alpha = 0.15 if i % 5 == 0 else 0.08
        lw = 0.4 if i % 5 == 0 else 0.2
        ax.axhline(y=i * 0.25, color='#ffaaaa', linewidth=lw, alpha=alpha)
    for i in range(cols * 2):
        alpha = 0.15 if i % 5 == 0 else 0.08
        lw = 0.4 if i % 5 == 0 else 0.2
        ax.axvline(x=i * 0.2, color='#ffaaaa', linewidth=lw, alpha=alpha)

def generate_ecg_wave(t, beats, p_wave_func=None, qrs_func=None, t_wave_func=None, 
                       st_func=None, pr_func=None, noise_level=0.01, beat_interval=0.8):
    """توليد إشارة ECG قابلة للتخصيص"""
    ecg = np.zeros_like(t)
    for beat_idx, t0 in enumerate(beats):
        if t0 > t[-1] - 0.5:
            continue
        idx = (t >= t0) & (t < t0 + beat_interval)
        rel_t = t[idx] - t0
        
        wave = np.zeros_like(rel_t)
        
        # P wave
        if p_wave_func:
            wave += p_wave_func(rel_t)
        else:
            wave += 0.12 * np.exp(-((rel_t - 0.08) ** 2) / 0.0012)
        
        # PR segment depression
        if pr_func:
            wave += pr_func(rel_t)
        
        # QRS complex
        if qrs_func:
            wave += qrs_func(rel_t)
        else:
            qrs = 1.0 * np.exp(-((rel_t - 0.20) ** 2) / 0.0004)
            qrs += -0.25 * np.exp(-((rel_t - 0.18) ** 2) / 0.00025)
            qrs += -0.2 * np.exp(-((rel_t - 0.22) ** 2) / 0.00025)
            wave += qrs
        
        # ST segment
        if st_func:
            wave += st_func(rel_t)
        
        # T wave
        if t_wave_func:
            wave += t_wave_func(rel_t)
        else:
            wave += 0.3 * np.exp(-((rel_t - 0.40) ** 2) / 0.005)
        
        ecg[idx] += wave
    
    ecg += np.random.normal(0, noise_level, len(ecg))
    return ecg

def generate_multi_lead(name, category, variations=3, **kwargs):
    """توليد عدة صور لنفس المرض"""
    folder = os.path.join(OUTPUT_DIR, category)
    os.makedirs(folder, exist_ok=True)
    
    for i in range(variations):
        fig, ax = plt.subplots(1, 1, figsize=(7, 5))
        draw_grid(ax)
        
        t = np.linspace(0, 4.5, 1200)
        beats = np.arange(0, 4.5, kwargs.get('beat_interval', 0.75) + random.uniform(-0.05, 0.05))
        
        ecg = generate_ecg_wave(t, beats, p_wave_func=kwargs.get("p_wave_func"), qrs_func=kwargs.get("qrs_func"), t_wave_func=kwargs.get("t_wave_func"), st_func=kwargs.get("st_func"), pr_func=kwargs.get("pr_func"), noise_level=kwargs.get("noise_level", 0.01))
        ax.plot(t, ecg, 'k-', linewidth=2.0)
        ax.set_xlim(0, 4.5)
        ax.set_ylim(-0.5, 1.5)
        
        title = kwargs.get('title', name).replace('_', ' ').title()
        save_ecg(fig, os.path.join(folder, f"{name}_{i+1}.png"), title)

# ==================== NORMAL SINUS RHYTHM (10 variations) ====================
print("🫀 Normal Sinus Rhythm...")
for i in range(10):
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    draw_grid(ax)
    t = np.linspace(0, 4.5, 1200)
    hr = random.randint(60, 85)
    beats = np.arange(0, 4.5, 60 / hr + random.uniform(-0.02, 0.02))
    ecg = generate_ecg_wave(t, beats, noise_level=0.015)
    ax.plot(t, ecg, 'k-', linewidth=2.0)
    ax.set_xlim(0, 4.5)
    ax.set_ylim(-0.5, 1.5)
    save_ecg(fig, os.path.join(OUTPUT_DIR, "normal", f"normal_{i+1}.png"), f"Normal Sinus Rhythm - {hr} bpm")

# ==================== SINUS BRADYCARDIA (3) ====================
print("🐢 Sinus Bradycardia...")
generate_multi_lead("sinus_bradycardia", "normal", 3, 
    beat_interval=1.1, title="Sinus Bradycardia - 48 bpm",
    noise_level=0.012)

# ==================== SINUS TACHYCARDIA (3) ====================
print("🐇 Sinus Tachycardia...")
generate_multi_lead("sinus_tachycardia", "normal", 3,
    beat_interval=0.55, title="Sinus Tachycardia - 110 bpm",
    noise_level=0.012)

# ==================== STEMI - ANTERIOR (4) ====================
print("💔 STEMI Anterior...")
for i in range(4):
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    draw_grid(ax)
    t = np.linspace(0, 4.5, 1200)
    beats = np.arange(0, 4.5, 0.75)
    ecg = generate_ecg_wave(t, beats,
        st_func=lambda rt: 0.35 * (rt > 0.22) * (rt < 0.38) + 0.1 * np.random.random(len(rt)),
        t_wave_func=lambda rt: 0.5 * np.exp(-((rt - 0.40) ** 2) / 0.006),
        noise_level=0.015)
    ax.plot(t, ecg, 'k-', linewidth=2.0)
    ax.set_xlim(0, 4.5)
    ax.set_ylim(-0.5, 1.8)
    save_ecg(fig, os.path.join(OUTPUT_DIR, "abnormal", f"stemi_anterior_{i+1}.png"), "STEMI - Anterior (ST Elevation V1-V4)")

# ==================== STEMI - INFERIOR (3) ====================
print("💔 STEMI Inferior...")
generate_multi_lead("stemi_inferior", "abnormal", 3,
    st_func=lambda rt: 0.3 * (rt > 0.22) * (rt < 0.38),
    t_wave_func=lambda rt: 0.45 * np.exp(-((rt - 0.40) ** 2) / 0.006),
    title="STEMI - Inferior (ST Elevation II, III, aVF)")

# ==================== ATRIAL FIBRILLATION (5) ====================
print("💓 Atrial Fibrillation...")
for i in range(5):
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    draw_grid(ax)
    t = np.linspace(0, 4.5, 1200)
    beats = np.cumsum(np.random.exponential(0.5, 10))
    ecg = generate_ecg_wave(t, beats,
        p_wave_func=lambda rt: np.zeros_like(rt),  # No P waves
        noise_level=0.02)
    # Add fibrillatory waves
    for t0 in beats:
        idx = (t >= t0) & (t < t0 + 0.4)
        fib = 0.04 * np.sin(2 * np.pi * 40 * t[idx]) * np.random.random(len(t[idx]))
        ecg[idx] += fib
    ax.plot(t, ecg, 'k-', linewidth=1.8)
    ax.set_xlim(0, 4.5)
    ax.set_ylim(-0.5, 1.5)
    save_ecg(fig, os.path.join(OUTPUT_DIR, "abnormal", f"afib_{i+1}.png"), "Atrial Fibrillation")

# ==================== ATRIAL FLUTTER (3) ====================
print("🔄 Atrial Flutter...")
generate_multi_lead("atrial_flutter", "abnormal", 3,
    p_wave_func=lambda rt: 0.15 * np.sin(2 * np.pi * 12 * rt) * (rt < 0.15),
    beat_interval=0.6, title="Atrial Flutter - Sawtooth Pattern")

# ==================== VENTRICULAR TACHYCARDIA (4) ====================
print("⚡ Ventricular Tachycardia...")
for i in range(4):
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    draw_grid(ax)
    t = np.linspace(0, 4.5, 1200)
    beats = np.arange(0, 4.5, 0.35)
    ecg = generate_ecg_wave(t, beats,
        p_wave_func=lambda rt: np.zeros_like(rt),
        qrs_func=lambda rt: 1.8 * np.exp(-((rt - 0.08) ** 2) / 0.0008),
        t_wave_func=lambda rt: -0.4 * np.exp(-((rt - 0.18) ** 2) / 0.003),
        noise_level=0.02)
    ax.plot(t, ecg, 'k-', linewidth=2.0)
    ax.set_xlim(0, 4.5)
    ax.set_ylim(-1.0, 2.0)
    save_ecg(fig, os.path.join(OUTPUT_DIR, "abnormal", f"vtach_{i+1}.png"), "Ventricular Tachycardia")

# ==================== TORSADES DE POINTES (2) ====================
print("🌀 Torsades de Pointes...")
for i in range(2):
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    draw_grid(ax)
    t = np.linspace(0, 4.5, 1200)
    beats = np.arange(0, 4.5, 0.35)
    ecg = generate_ecg_wave(t, beats, p_wave_func=lambda rt: np.zeros_like(rt),
        qrs_func=lambda rt: 1.5 * np.exp(-((rt - 0.08) ** 2) / 0.0006),
        noise_level=0.03)
    # Add sinusoidal twisting
    twist = 0.8 * np.sin(2 * np.pi * 0.3 * t) * np.sin(2 * np.pi * 5 * t)
    ecg = ecg * (1 + 0.5 * twist)
    ax.plot(t, ecg, 'k-', linewidth=1.8)
    ax.set_xlim(0, 4.5)
    ax.set_ylim(-2.0, 2.0)
    save_ecg(fig, os.path.join(OUTPUT_DIR, "abnormal", f"torsades_{i+1}.png"), "Torsades de Pointes")

# ==================== AV BLOCKS (6 - 2 each type) ====================
print("🔌 AV Blocks...")
# 1st Degree
generate_multi_lead("av_block_1st", "abnormal", 2,
    p_wave_func=lambda rt: 0.12 * np.exp(-((rt - 0.08) ** 2) / 0.001),
    beat_interval=0.8, title="AV Block - 1st Degree (PR Prolongation)")

# 2nd Degree Type I (Wenckebach)
for i in range(2):
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    draw_grid(ax)
    t = np.linspace(0, 4.5, 1200)
    ecg = np.zeros_like(t)
    t0 = 0
    pr = 0.16
    while t0 < 4.2:
        idx = (t >= t0) & (t < t0 + 0.7)
        rel_t = t[idx] - t0
        p_wave = 0.12 * np.exp(-((rel_t - pr - 0.02) ** 2) / 0.001)
        qrs = 1.0 * np.exp(-((rel_t - pr - 0.08) ** 2) / 0.0004)
        t_wave = 0.3 * np.exp(-((rel_t - pr - 0.25) ** 2) / 0.005)
        ecg[idx] += p_wave + qrs + t_wave
        pr += 0.06
        if pr > 0.35:
            pr = 0.16
            t0 += 1.2
        else:
            t0 += 0.7
    ax.plot(t, ecg, 'k-', linewidth=1.8)
    ax.set_xlim(0, 4.5)
    ax.set_ylim(-0.5, 1.5)
    save_ecg(fig, os.path.join(OUTPUT_DIR, "abnormal", f"wenckebach_{i+1}.png"), "AV Block - 2nd Degree Type I (Wenckebach)")

# 3rd Degree (Complete)
generate_multi_lead("complete_heart_block", "abnormal", 2,
    p_wave_func=lambda rt: 0.12 * np.sin(2 * np.pi * 3.5 * rt) * (rt < 0.5) + 0.12 * np.exp(-((rt % 0.28 - 0.05) ** 2) / 0.0005),
    beat_interval=0.9, title="AV Block - 3rd Degree (Complete Heart Block)")

# ==================== BUNDLE BRANCH BLOCKS (4) ====================
print("📊 Bundle Branch Blocks...")
generate_multi_lead("rbbb", "abnormal", 2,
    qrs_func=lambda rt: 1.3 * np.exp(-((rt - 0.24) ** 2) / 0.0006),
    title="Right Bundle Branch Block (RSR' in V1)")
generate_multi_lead("lbbb", "abnormal", 2,
    qrs_func=lambda rt: 1.5 * np.exp(-((rt - 0.26) ** 2) / 0.0008),
    title="Left Bundle Branch Block")

# ==================== HYPERKALEMIA (3) ====================
print("⚠️ Hyperkalemia...")
generate_multi_lead("hyperkalemia", "abnormal", 3,
    p_wave_func=lambda rt: np.zeros_like(rt),
    qrs_func=lambda rt: 0.8 * np.exp(-((rt - 0.24) ** 2) / 0.001),
    t_wave_func=lambda rt: 1.2 * np.exp(-((rt - 0.38) ** 2) / 0.0008),
    title="Hyperkalemia - Peaked T Waves + Wide QRS")

# ==================== HYPOKALEMIA (2) ====================
print("🔻 Hypokalemia...")
generate_multi_lead("hypokalemia", "abnormal", 2,
    t_wave_func=lambda rt: 0.1 * np.exp(-((rt - 0.42) ** 2) / 0.008),
    noise_level=0.02,
    title="Hypokalemia - Flat T Waves + Prominent U Waves")

# ==================== WELLENS SYNDROME (2) ====================
print("📉 Wellens Syndrome...")
generate_multi_lead("wellens", "abnormal", 2,
    t_wave_func=lambda rt: -0.6 * np.exp(-((rt - 0.38) ** 2) / 0.004),
    title="Wellens Syndrome - Deep T Wave Inversion V2-V3")

# ==================== PERICARDITIS (3) ====================
print("🔥 Pericarditis...")
generate_multi_lead("pericarditis", "abnormal", 3,
    st_func=lambda rt: 0.25 * (rt > 0.18) * (rt < 0.42),
    pr_func=lambda rt: -0.06 * (rt > 0.02) * (rt < 0.16),
    title="Pericarditis - Diffuse ST Elevation + PR Depression")

# ==================== LONG QT (3) ====================
print("⏱ Long QT...")
generate_multi_lead("long_qt", "abnormal", 3,
    beat_interval=1.0,
    t_wave_func=lambda rt: 0.4 * np.exp(-((rt - 0.55) ** 2) / 0.008),
    title="Long QT Syndrome - Prolonged QTc")

# ==================== WPW (3) ====================
print("⚡ WPW...")
generate_multi_lead("wpw", "abnormal", 3,
    qrs_func=lambda rt: 1.5 * np.exp(-((rt - 0.15) ** 2) / 0.0006),
    beat_interval=0.72,
    title="WPW Syndrome - Delta Wave + Short PR")

# ==================== BRUGADA (2) ====================
print("🧬 Brugada...")
generate_multi_lead("brugada", "abnormal", 2,
    st_func=lambda rt: 0.5 * np.exp(-((rt - 0.24) ** 2) / 0.003),
    t_wave_func=lambda rt: -0.4 * np.exp(-((rt - 0.40) ** 2) / 0.004),
    title="Brugada Syndrome - Coved ST Elevation V1-V2")

# ==================== S1Q3T3 (PE Pattern) (2) ====================
print("🫁 S1Q3T3...")
generate_multi_lead("s1q3t3", "abnormal", 2,
    qrs_func=lambda rt: 0.6 * np.exp(-((rt - 0.22) ** 2) / 0.0005),
    t_wave_func=lambda rt: -0.3 * np.exp(-((rt - 0.38) ** 2) / 0.006),
    title="S1Q3T3 Pattern - Suggestive of Pulmonary Embolism")

# ==================== LVH (3) ====================
print("💪 LVH...")
generate_multi_lead("lvh", "abnormal", 3,
    qrs_func=lambda rt: 1.8 * np.exp(-((rt - 0.20) ** 2) / 0.0005) + -0.5 * np.exp(-((rt - 0.18) ** 2) / 0.0003),
    t_wave_func=lambda rt: -0.35 * np.exp(-((rt - 0.40) ** 2) / 0.005),
    title="Left Ventricular Hypertrophy with Strain")

# ==================== PACED RHYTHM (2) ====================
print("🔋 Paced Rhythm...")
for i in range(2):
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    draw_grid(ax)
    t = np.linspace(0, 4.5, 1200)
    beats = np.arange(0, 4.5, 0.85)
    ecg = generate_ecg_wave(t, beats,
        p_wave_func=lambda rt: np.zeros_like(rt),
        qrs_func=lambda rt: 2.0 * np.exp(-((rt - 0.10) ** 2) / 0.001),
        t_wave_func=lambda rt: 0.5 * np.exp(-((rt - 0.35) ** 2) / 0.006))
    # Add pacing spikes
    for t0 in beats:
        spike_idx = (t >= t0 - 0.01) & (t <= t0 + 0.01)
        ecg[spike_idx] = 2.5
    ax.plot(t, ecg, 'k-', linewidth=1.8)
    ax.set_xlim(0, 4.5)
    ax.set_ylim(-0.5, 2.5)
    save_ecg(fig, os.path.join(OUTPUT_DIR, "abnormal", f"paced_{i+1}.png"), "Ventricular Paced Rhythm")

# ==================== ATRIAL ENLARGEMENT (2) ====================
print("📏 Atrial Enlargement...")
generate_multi_lead("atrial_enlargement", "abnormal", 2,
    p_wave_func=lambda rt: 0.25 * np.exp(-((rt - 0.10) ** 2) / 0.002),
    title="Left Atrial Enlargement - P Mitrale")

# ==================== FINAL SUMMARY ====================
print("\n" + "="*50)
print("🎉 ECG Library Generation Complete!")
# Count images
normal_count = len(os.listdir(os.path.join(OUTPUT_DIR, "normal")))
abnormal_count = len(os.listdir(os.path.join(OUTPUT_DIR, "abnormal")))
print(f"📊 Normal: {normal_count} images")
print(f"📊 Abnormal: {abnormal_count} images")
print(f"📊 TOTAL: {normal_count + abnormal_count} ECG images")
print("="*50)
