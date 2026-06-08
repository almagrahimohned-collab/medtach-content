import json, os
from pathlib import Path

# Disease → Condition + Concept mapping
DISEASE_MAP = {
    'acute coronary syndrome': ('Acute Coronary Syndrome', 'ECG interpretation'),
    'acs': ('Acute Coronary Syndrome', 'ECG interpretation'),
    'stemi': ('STEMI', 'Emergency diagnosis'),
    'heart failure': ('Heart Failure', 'Diagnosis'),
    'atrial fibrillation': ('Atrial Fibrillation', 'Rhythm interpretation'),
    'pneumonia': ('Pneumonia', 'Imaging interpretation'),
    'pulmonary embolism': ('Pulmonary Embolism', 'Diagnosis'),
    'stroke': ('Stroke', 'Emergency diagnosis'),
    'copd': ('COPD', 'Management'),
    'asthma': ('Asthma', 'Management'),
    'diabetes': ('Diabetes', 'Management'),
    'dka': ('DKA', 'Emergency management'),
    'hypertension': ('Hypertension', 'Management'),
    'sepsis': ('Sepsis', 'Emergency management'),
    'meningitis': ('Meningitis', 'Emergency diagnosis'),
    'aki': ('Acute Kidney Injury', 'Diagnosis'),
    'ckd': ('Chronic Kidney Disease', 'Management'),
    'anemia': ('Anemia', 'Diagnosis'),
    'thyroid': ('Thyroid Disorders', 'Diagnosis'),
    'cirrhosis': ('Cirrhosis', 'Management'),
}

for root, dirs, files in os.walk('../questions'):
    for file in files:
        if not file.endswith('.json'): continue
        fp = Path(root) / file
        with open(fp) as f: q = json.load(f)
        
        topic = q.get('topic', '').lower()
        system = q.get('system', '').lower()
        
        # Find match
        for key, (condition, concept) in DISEASE_MAP.items():
            if key in topic or key in system:
                q['condition'] = condition
                q['concept'] = concept
                break
        
        if not q.get('condition'):
            q['condition'] = q.get('topic', system).title()
            q['concept'] = 'General'
        
        with open(fp, 'w') as f: json.dump(q, f, indent=2)

print("✅ Conditions & concepts fixed!")
