#!/usr/bin/env python3
"""إصلاح الحالات الناقصة hidden_data"""

import json
from pathlib import Path

CASES_DIR = Path("..")

# الحالات اللي محتاجة hidden_data
missing_cases = [
    "cases/pediatrics/general/kawasaki_refractory.json",
    "cases/surgery/cardiothoracic/cardiac_tamponade_trauma.json",
    "cases/surgery/general/acute_appendicitis.json",
    "cases/surgery/general/fournier_gangrene.json",
    "cases/surgery/general/perforated_diverticulitis.json",
    "cases/surgery/orthopedics/compartment_syndrome.json",
]

for case_path in missing_cases:
    filepath = CASES_DIR / case_path
    if not filepath.exists():
        print(f"❌ Not found: {case_path}")
        continue
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    if 'hidden_data' not in data:
        data['hidden_data'] = {}
    
    # إضافة تحاليل أساسية حسب التخصص
    spec = data.get('specialty', '')
    title = data.get('title', '').lower()
    patient = data.get('patient', {})
    age = patient.get('age', 45)
    gender = patient.get('gender', 'male')
    
    # CBC أساسي
    data['hidden_data']['cbc'] = f"WBC: 12,500 /µL | RBC: 4.5 M/µL | Hb: 13.8 g/dL | Hct: 41% | MCV: 88 fL | Platelets: 250,000 /µL"
    data['hidden_data']['cmp'] = f"Na: 140 mmol/L | K: 4.0 mmol/L | Cl: 103 mmol/L | HCO3: 24 mmol/L | BUN: 15 mg/dL | Cr: 1.0 mg/dL | Glucose: 100 mg/dL | Ca: 9.5 mg/dL | Alb: 4.2 g/dL | AST: 28 U/L | ALT: 32 U/L | ALP: 75 U/L | T.Bil: 0.7 mg/dL"
    
    if spec in ['cardiology', 'surgery'] and ('tamponade' in title or 'cardiac' in title):
        data['hidden_data']['ecg'] = "Low voltage QRS, electrical alternans, sinus tachycardia"
        data['hidden_data']['echo'] = "Large pericardial effusion with RV diastolic collapse"
        data['hidden_data']['cxr'] = "Enlarged cardiac silhouette, clear lung fields"
    
    if 'appendicitis' in title:
        data['hidden_data']['ct_abdomen'] = "Dilated appendix 12mm with wall thickening and periappendiceal fat stranding"
        data['hidden_data']['crp'] = "CRP: 85 mg/L (elevated)"
    
    if 'fournier' in title or 'gangrene' in title:
        data['hidden_data']['ct_abdomen'] = "Extensive gas in scrotum, perineum, and abdominal wall"
        data['hidden_data']['crp'] = "CRP: 250 mg/L (severely elevated)"
        data['hidden_data']['lactate'] = "Lactate: 6.5 mmol/L"
    
    if 'diverticulitis' in title or 'perforated' in title:
        data['hidden_data']['ct_abdomen'] = "Perforated sigmoid diverticulitis with pneumoperitoneum and free fluid"
        data['hidden_data']['lactate'] = "Lactate: 4.2 mmol/L"
    
    if 'compartment' in title:
        data['hidden_data']['compartment_pressure'] = "Anterior compartment: 65mmHg, Lateral: 55mmHg, Deep posterior: 48mmHg"
        data['hidden_data']['ck'] = "CK: 2,500 U/L (elevated)"
        data['hidden_data']['xray'] = "Comminuted tibial shaft fracture"
    
    if 'kawasaki' in title:
        data['hidden_data']['echo'] = "RCA Z-score 3.5, mild coronary dilation"
        data['hidden_data']['crp'] = "CRP: 180 mg/L"
        data['hidden_data']['esr'] = "ESR: 95 mm/hr"
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Fixed: {case_path}")

print("\n🎉 All cases fixed!")
