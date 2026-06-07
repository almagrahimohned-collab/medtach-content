import matplotlib.pyplot as plt
import numpy as np
import os

# إعدادات الصورة
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['lines.linewidth'] = 1.5
plt.rcParams['font.size'] = 10

OUTPUT_DIR = "../media/ecg"

def generate_normal_ecg(filename, rate=72, title="Normal Sinus Rhythm"):
    """توليد صورة ECG طبيعية"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    
    # رسم شبكة
    for i in range(0, 10):
        ax.axhline(y=i*0.5, color='#ffcccc', linewidth=0.3)
    for i in range(0, 20):
        ax.axvline(x=i*0.2, color='#ffcccc', linewidth=0.3)
    for i in range(0, 10):
        ax.axhline(y=i*1.0, color='#ffaaaa', linewidth=0.5)
    for i in range(0, 20):
        ax.axvline(x=i*1.0, color='#ffaaaa', linewidth=0.5)
    
    # توليد إشارة ECG
    t = np.linspace(0, 5, 1000)
    hr = rate / 60
    ecg = np.zeros_like(t)
    
    for beat in range(6):
        t0 = beat / hr
        if t0 < 4.5:
            idx = (t >= t0) & (t < t0 + 0.8)
            rel_t = t[idx] - t0
            
            # P wave
            p_wave = 0.15 * np.exp(-((rel_t - 0.08) ** 2) / 0.001)
            # QRS complex
            qrs = 1.0 * np.exp(-((rel_t - 0.20) ** 2) / 0.0003)
            qrs += -0.3 * np.exp(-((rel_t - 0.18) ** 2) / 0.0002)
            qrs += -0.2 * np.exp(-((rel_t - 0.22) ** 2) / 0.0002)
            # T wave
            t_wave = 0.35 * np.exp(-((rel_t - 0.40) ** 2) / 0.004)
            
            ecg[idx] = p_wave + qrs + t_wave
    
    # إضافة اختلافات عشوائية بسيطة
    ecg += np.random.normal(0, 0.02, len(ecg))
    
    ax.plot(t, ecg, 'k-', linewidth=2)
    
    ax.set_xlim(0, 5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
    ax.set_xlabel(f'Rate: {rate} bpm | PR: {160 + np.random.randint(-10,10)}ms | QRS: {88 + np.random.randint(-5,5)}ms | QTc: {410 + np.random.randint(-10,10)}ms', fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=100, bbox_inches='tight')
    plt.close()
    print(f"✅ Generated: {filename}")

def generate_stemi_anterior(filename):
    """توليد صورة STEMI"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    
    for i in range(0, 10):
        ax.axhline(y=i*0.5, color='#ffcccc', linewidth=0.3)
        ax.axhline(y=i*1.0, color='#ffaaaa', linewidth=0.5)
    for i in range(0, 20):
        ax.axvline(x=i*0.2, color='#ffcccc', linewidth=0.3)
        ax.axvline(x=i*1.0, color='#ffaaaa', linewidth=0.5)
    
    t = np.linspace(0, 5, 1000)
    ecg = np.zeros_like(t)
    
    for beat in range(6):
        t0 = beat / 1.2
        if t0 < 4.5:
            idx = (t >= t0) & (t < t0 + 0.8)
            rel_t = t[idx] - t0
            
            # ST elevation
            p_wave = 0.15 * np.exp(-((rel_t - 0.08) ** 2) / 0.001)
            qrs = 1.2 * np.exp(-((rel_t - 0.20) ** 2) / 0.0003)
            qrs += -0.3 * np.exp(-((rel_t - 0.18) ** 2) / 0.0002)
            st_elevation = 0.4 * np.ones(len(rel_t)) * (rel_t > 0.22) * (rel_t < 0.38)
            t_wave = 0.5 * np.exp(-((rel_t - 0.40) ** 2) / 0.004)
            
            ecg[idx] = p_wave + qrs + st_elevation + t_wave
    
    ax.plot(t, ecg, 'k-', linewidth=2)
    ax.fill_between(t[300:700], -0.5, 1.5, where=(ecg[300:700] > 0.2), color='red', alpha=0.15)
    ax.set_xlim(0, 5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title("STEMI - Anterior (ST Elevation in V1-V4)", fontsize=14, fontweight='bold', color='red', pad=10)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "abnormal/stemi_anterior.png"), dpi=100, bbox_inches='tight')
    plt.close()
    print("✅ Generated: STEMI")

def generate_afib(filename):
    """توليد صورة Atrial Fibrillation"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    
    for i in range(0, 10):
        ax.axhline(y=i*0.5, color='#ffcccc', linewidth=0.3)
        ax.axhline(y=i*1.0, color='#ffaaaa', linewidth=0.5)
    
    t = np.linspace(0, 5, 1000)
    ecg = np.zeros_like(t)
    
    # AFib = irregular rhythm + no P waves
    beats = np.cumsum(np.random.exponential(0.7, 8))
    for t0 in beats:
        if t0 < 4.5:
            idx = (t >= t0) & (t < t0 + 0.4)
            rel_t = t[idx] - t0
            qrs = 1.0 * np.exp(-((rel_t - 0.15) ** 2) / 0.0003)
            t_wave = 0.3 * np.exp(-((rel_t - 0.30) ** 2) / 0.004)
            ecg[idx] = qrs + t_wave
            # fibrillation waves
            fib = 0.05 * np.sin(rel_t * 50) * (rel_t < 0.12)
            ecg[idx] += fib
    
    ax.plot(t, ecg, 'k-', linewidth=2)
    ax.set_xlim(0, 5)
    ax.set_ylim(-0.5, 1.2)
    ax.set_title("Atrial Fibrillation (Irregular, No P Waves)", fontsize=14, fontweight='bold', pad=10)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "abnormal/afib.png"), dpi=100, bbox_inches='tight')
    plt.close()
    print("✅ Generated: AFib")

# إنشاء المجلدات
os.makedirs(os.path.join(OUTPUT_DIR, "normal"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "abnormal"), exist_ok=True)

# توليد صور طبيعية
for i in range(5):
    generate_normal_ecg(f"normal/normal_{i+1}.png", rate=68 + np.random.randint(0,15))

# توليد صور مرضية
generate_stemi_anterior("abnormal/stemi_anterior.png")
generate_afib("abnormal/afib.png")

print("\n🎉 All ECG images generated!")
