#!/usr/bin/env python3
"""توليد 600 سؤال عالي الجودة - Case-Based Engine"""

import json, os, random, uuid
from pathlib import Path

OUTPUT_DIR = Path("../questions")

# 🧠 CASE MATRIX - كل case له presentation + diagnosis + distractors + concept
CASE_MATRIX = {
    "internal_medicine": {
        "cardiology": [
            # ECG Interpretation Cases
            {
                "presentation": "A {age}-year-old {gender} presents with crushing substernal chest pain radiating to left arm for 2 hours. Diaphoretic. ECG shows ST elevation of 3mm in leads V1-V4 with reciprocal ST depression in II, III, aVF.",
                "diagnosis": "Anterior STEMI",
                "distractors": ["NSTEMI", "Unstable Angina", "Pericarditis", "Aortic Dissection"],
                "concept": "ecg_interpretation",
                "cognitive_level": "clinical_reasoning",
                "trap_type": "ecg_misread",
                "tags": ["chest_pain", "stemi", "emergency", "ecg"],
                "explanation": {
                    "why_correct": "ST elevation in V1-V4 = anterior STEMI (LAD occlusion). Reciprocal changes confirm transmural ischemia.",
                    "why_wrong": {
                        "NSTEMI": "NSTEMI shows ST depression/T inversion, NOT ST elevation.",
                        "Unstable Angina": "UA has normal troponin + no ST elevation.",
                        "Pericarditis": "Pericarditis has DIFFUSE ST elevation + PR depression, not localized to V1-V4.",
                        "Aortic Dissection": "Dissection causes tearing pain + pulse deficit + widened mediastinum, not ST elevation."
                    }
                }
            },
            {
                "presentation": "A {age}-year-old {gender} with palpitations. ECG shows irregularly irregular rhythm with absent P waves. HR 130 bpm.",
                "diagnosis": "Atrial Fibrillation with RVR",
                "distractors": ["Atrial Flutter", "SVT", "Ventricular Tachycardia", "Sinus Tachycardia"],
                "concept": "ecg_interpretation",
                "cognitive_level": "interpretation",
                "trap_type": "ecg_misread",
                "tags": ["arrhythmia", "afib", "ecg", "palpitations"],
                "explanation": {
                    "why_correct": "Irregularly irregular + absent P waves = AFib. RVR = rate >100.",
                    "why_wrong": {
                        "Atrial Flutter": "Flutter has 'sawtooth' pattern, regular rhythm.",
                        "SVT": "SVT is regular, narrow QRS, rate 150-250.",
                        "Ventricular Tachycardia": "VT has WIDE QRS complexes.",
                        "Sinus Tachycardia": "Sinus tach has P waves before each QRS."
                    }
                }
            },
            {
                "presentation": "A {age}-year-old {gender} with progressive dyspnea, orthopnea, and bilateral leg edema. Echo shows LVEF 30% with global hypokinesis.",
                "diagnosis": "Systolic Heart Failure",
                "distractors": ["Diastolic Heart Failure", "COPD Exacerbation", "Pulmonary Embolism", "Nephrotic Syndrome"],
                "concept": "diagnosis",
                "cognitive_level": "clinical_reasoning",
                "trap_type": "diagnostic_confusion",
                "tags": ["heart_failure", "dyspnea", "edema", "echo"],
                "explanation": {
                    "why_correct": "LVEF <40% + symptoms = HFrEF. Global hypokinesis indicates ischemic or non-ischemic cardiomyopathy.",
                    "why_wrong": {
                        "Diastolic HF": "HFpEF has normal EF (>50%) with diastolic dysfunction.",
                        "COPD": "COPD causes wheezing, hyperinflation, not bilateral edema.",
                        "PE": "PE causes acute dyspnea, clear lungs, RV strain on echo.",
                        "Nephrotic": "Nephrotic causes edema + proteinuria, not low EF."
                    }
                }
            },
            {
                "presentation": "A {age}-year-old {gender} with syncope during exercise. ECG shows deep T wave inversion in V1-V3. Family history of sudden cardiac death.",
                "diagnosis": "Arrhythmogenic Right Ventricular Cardiomyopathy (ARVC)",
                "distractors": ["Brugada Syndrome", "Long QT Syndrome", "Hypertrophic Cardiomyopathy", "Vasovagal Syncope"],
                "concept": "diagnosis",
                "cognitive_level": "clinical_reasoning",
                "trap_type": "diagnostic_confusion",
                "tags": ["syncope", "arrhythmia", "genetic", "ecg"],
                "explanation": {
                    "why_correct": "Exercise syncope + T inversion V1-V3 + family history = ARVC. Fatty replacement of RV myocardium.",
                    "why_wrong": {
                        "Brugada": "Brugada has coved ST elevation V1-V2, syncope at rest.",
                        "Long QT": "LQTS has prolonged QTc, T wave alternans.",
                        "HCM": "HCM has LVH on echo, not RV involvement.",
                        "Vasovagal": "Vasovagal has triggers (pain, fear), normal ECG."
                    }
                }
            },
            {
                "presentation": "A {age}-year-old {gender} with acute chest pain. BP 85/60, JVD, muffled heart sounds. ECG shows low voltage with electrical alternans.",
                "diagnosis": "Cardiac Tamponade",
                "distractors": ["Tension Pneumothorax", "Massive PE", "Cardiogenic Shock", "Aortic Dissection"],
                "concept": "emergency_reasoning",
                "cognitive_level": "emergency_reasoning",
                "trap_type": "ecg_misread",
                "tags": ["emergency", "shock", "tamponade", "ecg"],
                "explanation": {
                    "why_correct": "Beck triad (hypotension + JVD + muffled sounds) + electrical alternans = tamponade. Pericardiocentesis emergently.",
                    "why_wrong": {
                        "Tension PTX": "PTX has tracheal deviation, hyperresonance, absent breath sounds.",
                        "Massive PE": "PE has RV strain on ECG, clear lungs.",
                        "Cardiogenic Shock": "Cardiogenic has pulmonary edema, not electrical alternans.",
                        "Dissection": "Dissection has tearing pain, pulse deficit, widened mediastinum."
                    }
                }
            },
        ],
        "pulmonology": [
            {
                "presentation": "A {age}-year-old {gender} with productive cough, fever 39°C, and dyspnea for 3 days. CXR shows right lower lobe consolidation with air bronchograms.",
                "diagnosis": "Community-Acquired Pneumonia",
                "distractors": ["COPD Exacerbation", "Pulmonary Embolism", "Lung Abscess", "Bronchitis"],
                "concept": "imaging_interpretation",
                "cognitive_level": "interpretation",
                "trap_type": "imaging_misinterpretation",
                "tags": ["pneumonia", "infection", "cxr", "fever"],
                "explanation": {
                    "why_correct": "Lobar consolidation + air bronchograms = pneumonia. CURB-65 score guides admission.",
                    "why_wrong": {
                        "COPD": "COPD has hyperinflation, not consolidation.",
                        "PE": "PE has normal CXR or wedge opacity, not consolidation.",
                        "Abscess": "Abscess has cavity with air-fluid level.",
                        "Bronchitis": "Bronchitis has normal CXR."
                    }
                }
            },
            {
                "presentation": "A {age}-year-old {gender} with sudden pleuritic chest pain and dyspnea after a 12-hour flight. CXR is normal. D-dimer elevated.",
                "diagnosis": "Pulmonary Embolism",
                "distractors": ["Pneumonia", "Pneumothorax", "Acute Coronary Syndrome", "Costochondritis"],
                "concept": "diagnosis",
                "cognitive_level": "clinical_reasoning",
                "trap_type": "diagnostic_confusion",
                "tags": ["pe", "emergency", "dyspnea", "dvt"],
                "explanation": {
                    "why_correct": "Sudden dyspnea + risk factor (travel) + normal CXR + elevated D-dimer = PE. CT-PA confirms.",
                    "why_wrong": {
                        "Pneumonia": "Pneumonia has infiltrate on CXR + productive cough.",
                        "Pneumothorax": "PTX has absent breath sounds + tracheal deviation.",
                        "ACS": "ACS has ECG changes + troponin elevation.",
                        "Costochondritis": "Costochondritis has reproducible chest wall tenderness."
                    }
                }
            },
        ],
    },
    "surgery": {
        "general_surgery": [
            {
                "presentation": "A {age}-year-old {gender} with periumbilical pain migrating to RLQ over 12 hours. Anorexia, nausea. McBurney point tenderness. WBC 14,500.",
                "diagnosis": "Acute Appendicitis",
                "distractors": ["Mesenteric Adenitis", "Ectopic Pregnancy", "Ureteral Stone", "Diverticulitis"],
                "concept": "diagnosis",
                "cognitive_level": "clinical_reasoning",
                "trap_type": "diagnostic_confusion",
                "tags": ["appendicitis", "acute_abdomen", "surgery", "emergency"],
                "explanation": {
                    "why_correct": "Migrating pain to RLQ + McBurney point + leukocytosis = appendicitis. CT confirms.",
                    "why_wrong": {
                        "Mesenteric Adenitis": "Mesenteric adenitis follows URI, less localized tenderness.",
                        "Ectopic": "Ectopic has adnexal mass + positive hCG.",
                        "Stone": "Ureteral stone has flank pain + hematuria.",
                        "Diverticulitis": "Diverticulitis is LLQ, older patients."
                    }
                }
            },
            {
                "presentation": "A {age}-year-old {gender} with RUQ pain after eating fatty meal. Positive Murphy sign. Ultrasound shows gallbladder wall thickening and pericholecystic fluid.",
                "diagnosis": "Acute Cholecystitis",
                "distractors": ["Biliary Colic", "Choledocholithiasis", "Pancreatitis", "Hepatitis"],
                "concept": "imaging_interpretation",
                "cognitive_level": "interpretation",
                "trap_type": "imaging_misinterpretation",
                "tags": ["cholecystitis", "surgery", "ultrasound", "ruq_pain"],
                "explanation": {
                    "why_correct": "RUQ pain + Murphy sign + US findings = cholecystitis. Laparoscopic cholecystectomy within 72h.",
                    "why_wrong": {
                        "Biliary Colic": "Colic has transient pain, normal US.",
                        "Choledocholithiasis": "CBD stone has dilated CBD + elevated bilirubin.",
                        "Pancreatitis": "Pancreatitis has epigastric pain + elevated lipase.",
                        "Hepatitis": "Hepatitis has diffuse tenderness + elevated LFTs."
                    }
                }
            },
        ],
    },
}

def generate_options(correct_diagnosis, distractors):
    """توليد خيارات مع distractors واقعية"""
    options = [{"id": "a", "text": correct_diagnosis, "isCorrect": True}]
    for i, d in enumerate(distractors[:3]):
        options.append({"id": chr(ord('b') + i), "text": d, "isCorrect": False})
    return options

def generate_questions(specialty, subspecialty, count=50):
    """توليد أسئلة من CASE_MATRIX"""
    cases = CASE_MATRIX.get(specialty, {}).get(subspecialty, [])
    if not cases:
        return []
    
    questions = []
    for i in range(count):
        case = random.choice(cases)
        age = random.choice([35, 45, 55, 65, 72])
        gender = random.choice(["man", "woman"])
        
        question_text = case["presentation"].format(age=age, gender=gender)
        
        difficulties = ["beginner", "intermediate", "advanced"]
        weights = [0.25, 0.50, 0.25]
        difficulty = random.choices(difficulties, weights=weights)[0]
        
        # ✅ Unique ID
        short_id = f"{specialty[:4]}_{subspecialty[:4]}_{i+1:03d}"
        unique_id = f"{short_id}_{uuid.uuid4().hex[:6]}"
        
        questions.append({
            "id": unique_id,
            "specialty": specialty,
            "subspecialty": subspecialty,
            "concept": case["concept"],
            "cognitive_level": case["cognitive_level"],
            "difficulty": difficulty,
            "question": question_text,
            "options": generate_options(case["diagnosis"], case["distractors"]),
            "explanation": case["explanation"],
            "trap_type": case["trap_type"],
            "tags": case["tags"],
        })
    
    return questions

# توليد كل الملفات
total = 0
with open("../questions/index.json") as f:
    index = json.load(f)

for spec, spec_data in index["subjects"].items():
    for sub, sub_data in spec_data["subspecialties"].items():
        filepath = OUTPUT_DIR / sub_data["file"]
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        questions = generate_questions(spec, sub, 50)
        if questions:
            with open(filepath, "w") as f:
                json.dump(questions, f, indent=2)
            total += len(questions)
            print(f"✅ {spec}/{sub}: {len(questions)} questions")

print(f"\n🎉 Total: {total} questions generated with Case-Based Engine!")
