#!/usr/bin/env python3
"""توليد 600 سؤال كامل - كل الـ 12 subspecialty"""

import json, os, random, uuid
from pathlib import Path

OUTPUT_DIR = Path("../questions")

# 🧠 CASE MATRIX كامل - 12 subspecialty
CASE_MATRIX = {
    "internal_medicine": {
        "cardiology": [
            {"presentation": "A {age}-year-old {gender} with crushing chest pain radiating to left arm. ECG: ST elevation V1-V4.", "diagnosis": "Anterior STEMI", "distractors": ["NSTEMI", "Pericarditis", "Aortic Dissection", "Unstable Angina"], "concept": "ecg_interpretation", "cognitive_level": "clinical_reasoning", "trap_type": "ecg_misread", "tags": ["chest_pain", "stemi", "emergency"]},
            {"presentation": "A {age}-year-old {gender} with palpitations. ECG: irregularly irregular, absent P waves, HR 130.", "diagnosis": "Atrial Fibrillation", "distractors": ["Atrial Flutter", "SVT", "Sinus Tachycardia", "Ventricular Tachycardia"], "concept": "ecg_interpretation", "cognitive_level": "interpretation", "trap_type": "ecg_misread", "tags": ["arrhythmia", "afib", "palpitations"]},
            {"presentation": "A {age}-year-old {gender} with progressive dyspnea, orthopnea, edema. Echo: LVEF 30%.", "diagnosis": "Systolic Heart Failure", "distractors": ["Diastolic HF", "COPD", "PE", "Nephrotic Syndrome"], "concept": "diagnosis", "cognitive_level": "clinical_reasoning", "trap_type": "diagnostic_confusion", "tags": ["heart_failure", "dyspnea", "edema"]},
            {"presentation": "A {age}-year-old {gender} with syncope during exercise. ECG: T inversion V1-V3. Family history SCD.", "diagnosis": "ARVC", "distractors": ["Brugada", "Long QT", "HCM", "Vasovagal"], "concept": "diagnosis", "cognitive_level": "clinical_reasoning", "trap_type": "diagnostic_confusion", "tags": ["syncope", "arrhythmia", "genetic"]},
            {"presentation": "A {age}-year-old {gender} with acute chest pain, BP 85/60, JVD, muffled heart sounds, electrical alternans.", "diagnosis": "Cardiac Tamponade", "distractors": ["Tension PTX", "Massive PE", "Cardiogenic Shock", "Aortic Dissection"], "concept": "emergency_reasoning", "cognitive_level": "emergency_reasoning", "trap_type": "ecg_misread", "tags": ["emergency", "shock", "tamponade"]},
        ],
        "pulmonology": [
            {"presentation": "A {age}-year-old {gender} with productive cough, fever 39°C, CXR: RLL consolidation.", "diagnosis": "CAP", "distractors": ["COPD", "PE", "Lung Abscess", "Bronchitis"], "concept": "imaging_interpretation", "cognitive_level": "interpretation", "trap_type": "imaging_misinterpretation", "tags": ["pneumonia", "fever", "cxr"]},
            {"presentation": "A {age}-year-old {gender} with sudden pleuritic pain after flight. CXR normal. D-dimer elevated.", "diagnosis": "Pulmonary Embolism", "distractors": ["Pneumonia", "PTX", "ACS", "Costochondritis"], "concept": "diagnosis", "cognitive_level": "clinical_reasoning", "trap_type": "diagnostic_confusion", "tags": ["pe", "emergency", "dyspnea"]},
            {"presentation": "A {age}-year-old {gender} smoker with chronic cough, wheezing, barrel chest. CXR: hyperinflation.", "diagnosis": "COPD", "distractors": ["Asthma", "Bronchiectasis", "CHF", "ILD"], "concept": "diagnosis", "cognitive_level": "interpretation", "trap_type": "imaging_misinterpretation", "tags": ["copd", "smoking", "wheezing"]},
            {"presentation": "A {age}-year-old {gender} with acute dyspnea, absent breath sounds left side, tracheal deviation.", "diagnosis": "Tension Pneumothorax", "distractors": ["PE", "PTX simple", "Tamponade", "Asthma"], "concept": "emergency_reasoning", "cognitive_level": "emergency_reasoning", "trap_type": "diagnostic_confusion", "tags": ["ptx", "emergency", "dyspnea"]},
            {"presentation": "A {age}-year-old {gender} with asthma history, wheezing, tachypnea, SpO2 88%.", "diagnosis": "Acute Asthma Exacerbation", "distractors": ["COPD", "Anaphylaxis", "PE", "Pneumonia"], "concept": "management", "cognitive_level": "clinical_reasoning", "trap_type": "diagnostic_confusion", "tags": ["asthma", "wheezing", "emergency"]},
        ],
        "gastroenterology": [
            {"presentation": "A {age}-year-old {gender} with epigastric pain radiating to back, nausea. Lipase 850.", "diagnosis": "Acute Pancreatitis", "distractors": ["Cholecystitis", "PUD", "Gastritis", "AAA"], "concept": "diagnosis", "cognitive_level": "clinical_reasoning", "trap_type": "lab_misinterpretation", "tags": ["pancreatitis", "lipase", "pain"]},
            {"presentation": "A {age}-year-old {gender} with hematemesis, melena, HR 110, BP 90/60. BUN 45.", "diagnosis": "Upper GI Bleeding", "distractors": ["Lower GI Bleed", "Pancreatitis", "PUD perforated", "Esophagitis"], "concept": "emergency_reasoning", "cognitive_level": "emergency_reasoning", "trap_type": "diagnostic_confusion", "tags": ["gi_bleed", "emergency", "shock"]},
            {"presentation": "A {age}-year-old {gender} with jaundice, ascites, spider angiomata. AST/ALT 2:1 ratio.", "diagnosis": "Alcoholic Cirrhosis", "distractors": ["Hepatitis B", "NASH", "Biliary Cirrhosis", "Hemochromatosis"], "concept": "diagnosis", "cognitive_level": "clinical_reasoning", "trap_type": "lab_misinterpretation", "tags": ["cirrhosis", "liver", "jaundice"]},
            {"presentation": "A {age}-year-old {gender} with bloody diarrhea, tenesmus, colonoscopy: continuous inflammation from rectum.", "diagnosis": "Ulcerative Colitis", "distractors": ["Crohn Disease", "Infectious Colitis", "IBS", "Celiac Disease"], "concept": "diagnosis", "cognitive_level": "clinical_reasoning", "trap_type": "diagnostic_confusion", "tags": ["ibd", "diarrhea", "colitis"]},
            {"presentation": "A {age}-year-old {gender} with RUQ pain after fatty meal, Murphy sign positive.", "diagnosis": "Acute Cholecystitis", "distractors": ["Biliary Colic", "Pancreatitis", "Hepatitis", "CBD Stone"], "concept": "imaging_interpretation", "cognitive_level": "interpretation", "trap_type": "imaging_misinterpretation", "tags": ["cholecystitis", "surgery", "ruq_pain"]},
        ],
    },
    "surgery": {
        "general_surgery": [
            {"presentation": "A {age}-year-old {gender} with RLQ pain, McBurney point tenderness, WBC 14.5K.", "diagnosis": "Acute Appendicitis", "distractors": ["Mesenteric Adenitis", "Ectopic", "Stone", "Diverticulitis"], "concept": "diagnosis", "cognitive_level": "clinical_reasoning", "trap_type": "diagnostic_confusion", "tags": ["appendicitis", "surgery", "emergency"]},
            {"presentation": "A {age}-year-old {gender} with reducible groin bulge, cough impulse positive.", "diagnosis": "Inguinal Hernia", "distractors": ["Femoral Hernia", "Hydrocele", "Lymphadenopathy", "Abscess"], "concept": "diagnosis", "cognitive_level": "interpretation", "trap_type": "diagnostic_confusion", "tags": ["hernia", "surgery"]},
            {"presentation": "A {age}-year-old {gender} with abdominal distension, vomiting, high-pitched bowel sounds, previous laparotomy.", "diagnosis": "Small Bowel Obstruction", "distractors": ["Ileus", "Gastroenteritis", "Pancreatitis", "Constipation"], "concept": "emergency_reasoning", "cognitive_level": "clinical_reasoning", "trap_type": "imaging_misinterpretation", "tags": ["obstruction", "surgery", "emergency"]},
        ],
        "trauma": [
            {"presentation": "A {age}-year-old {gender} with GSW to chest, absent breath sounds left, trachea deviated right.", "diagnosis": "Tension Pneumothorax", "distractors": ["Hemothorax", "Cardiac Tamponade", "PE", "Diaphragmatic Rupture"], "concept": "emergency_reasoning", "cognitive_level": "emergency_reasoning", "trap_type": "diagnostic_confusion", "tags": ["trauma", "ptx", "emergency"]},
            {"presentation": "A {age}-year-old {gender} with pelvic fracture after MVA, BP 80/50, HR 130, FAST positive.", "diagnosis": "Hemorrhagic Shock", "distractors": ["Neurogenic Shock", "Cardiogenic Shock", "Septic Shock", "Obstructive Shock"], "concept": "emergency_reasoning", "cognitive_level": "emergency_reasoning", "trap_type": "diagnostic_confusion", "tags": ["trauma", "shock", "hemorrhage"]},
        ],
        "vascular": [
            {"presentation": "A {age}-year-old {gender} with sudden severe leg pain, cold pale limb, absent pulses.", "diagnosis": "Acute Limb Ischemia", "distractors": ["DVT", "Compartment Syndrome", "Cellulitis", "Neuropathy"], "concept": "emergency_reasoning", "cognitive_level": "emergency_reasoning", "trap_type": "diagnostic_confusion", "tags": ["ischemia", "vascular", "emergency"]},
            {"presentation": "A {age}-year-old {gender} with pulsatile abdominal mass, sudden back pain, hypotension.", "diagnosis": "Ruptured AAA", "distractors": ["Renal Colic", "Pancreatitis", "Diverticulitis", "Aortic Dissection"], "concept": "emergency_reasoning", "cognitive_level": "emergency_reasoning", "trap_type": "diagnostic_confusion", "tags": ["aaa", "emergency", "vascular"]},
        ],
    },
    "pediatrics": {
        "neonatology": [
            {"presentation": "A 2-day-old with bilious vomiting, abdominal distension. XR: double bubble sign.", "diagnosis": "Duodenal Atresia", "distractors": ["Malrotation", "Hirschsprung", "NEC", "Pyloric Stenosis"], "concept": "diagnosis", "cognitive_level": "clinical_reasoning", "trap_type": "imaging_misinterpretation", "tags": ["neonate", "obstruction", "vomiting"]},
            {"presentation": "A 32-week preemie with respiratory distress, grunting, nasal flaring. CXR: ground glass.", "diagnosis": "RDS", "distractors": ["TTN", "Pneumonia", "Pneumothorax", "Meconium Aspiration"], "concept": "imaging_interpretation", "cognitive_level": "interpretation", "trap_type": "imaging_misinterpretation", "tags": ["neonate", "respiratory", "prematurity"]},
        ],
        "pediatric_infectious": [
            {"presentation": "A 6-month-old with fever 40°C, bulging fontanelle, neck stiffness.", "diagnosis": "Bacterial Meningitis", "distractors": ["Viral Meningitis", "Encephalitis", "Febrile Seizure", "Brain Abscess"], "concept": "emergency_reasoning", "cognitive_level": "emergency_reasoning", "trap_type": "diagnostic_confusion", "tags": ["meningitis", "fever", "emergency"]},
            {"presentation": "A 3-year-old with stridor, barking cough, respiratory distress.", "diagnosis": "Croup", "distractors": ["Epiglottitis", "Asthma", "Foreign Body", "Anaphylaxis"], "concept": "diagnosis", "cognitive_level": "clinical_reasoning", "trap_type": "diagnostic_confusion", "tags": ["croup", "stridor", "pediatric"]},
        ],
        "pediatric_emergency": [
            {"presentation": "A 2-year-old with sudden abdominal pain, currant jelly stool, palpable mass.", "diagnosis": "Intussusception", "distractors": ["Appendicitis", "Gastroenteritis", "Volvulus", "Constipation"], "concept": "emergency_reasoning", "cognitive_level": "emergency_reasoning", "trap_type": "diagnostic_confusion", "tags": ["intussusception", "emergency", "pediatric"]},
        ],
    },
    "obgyn": {
        "obstetrics": [
            {"presentation": "A 28-year-old G1P0 at 36 weeks with severe headache, BP 170/110, proteinuria 3+.", "diagnosis": "Severe Preeclampsia", "distractors": ["Eclampsia", "HELLP", "Gestational HTN", "Chronic HTN"], "concept": "emergency_reasoning", "cognitive_level": "emergency_reasoning", "trap_type": "diagnostic_confusion", "tags": ["preeclampsia", "pregnancy", "emergency"]},
            {"presentation": "A 32-year-old at 8 weeks with vaginal bleeding, cramping, closed cervix.", "diagnosis": "Threatened Abortion", "distractors": ["Inevitable Abortion", "Complete Abortion", "Ectopic", "Molar Pregnancy"], "concept": "diagnosis", "cognitive_level": "clinical_reasoning", "trap_type": "diagnostic_confusion", "tags": ["abortion", "pregnancy", "bleeding"]},
        ],
        "gynecology": [
            {"presentation": "A 24-year-old with acute unilateral pelvic pain, adnexal mass, positive hCG.", "diagnosis": "Ectopic Pregnancy", "distractors": ["Ovarian Cyst", "PID", "Appendicitis", "UTI"], "concept": "emergency_reasoning", "cognitive_level": "emergency_reasoning", "trap_type": "diagnostic_confusion", "tags": ["ectopic", "emergency", "gynecology"]},
        ],
        "reproductive": [
            {"presentation": "A 30-year-old with irregular periods, hirsutism, obesity, US: polycystic ovaries.", "diagnosis": "PCOS", "distractors": ["Cushing", "CAH", "Thyroid Disease", "Hyperprolactinemia"], "concept": "diagnosis", "cognitive_level": "clinical_reasoning", "trap_type": "diagnostic_confusion", "tags": ["pcos", "infertility", "hormones"]},
        ],
    },
}

def generate_options(correct, distractors):
    options = [{"id": "a", "text": correct, "isCorrect": True}]
    for i, d in enumerate(distractors[:3]):
        options.append({"id": chr(ord('b') + i), "text": d, "isCorrect": False})
    return options

def generate_explanation(correct, distractors, concept):
    why_wrong = {}
    for d in distractors[:3]:
        why_wrong[d] = f"{d} has different presentation and findings than {correct}."
    return {
        "why_correct": f"The presentation is classic for {correct}. This is a {concept} case requiring prompt recognition.",
        "why_wrong": why_wrong
    }

def generate_questions(specialty, subspecialty, count=50):
    cases = CASE_MATRIX.get(specialty, {}).get(subspecialty, [])
    if not cases:
        return []
    
    questions = []
    for i in range(count):
        case = random.choice(cases)
        age = random.choice([25, 35, 45, 55, 65, 72])
        gender = random.choice(["man", "woman"])
        
        question_text = case["presentation"].format(age=age, gender=gender)
        
        difficulties = ["beginner", "intermediate", "advanced"]
        weights = [0.25, 0.50, 0.25]
        difficulty = random.choices(difficulties, weights=weights)[0]
        
        unique_id = f"{specialty[:4]}_{subspecialty[:4]}_{i+1:03d}_{uuid.uuid4().hex[:6]}"
        
        questions.append({
            "id": unique_id,
            "specialty": specialty, "subspecialty": subspecialty,
            "concept": case["concept"], "cognitive_level": case["cognitive_level"],
            "difficulty": difficulty,
            "question": question_text,
            "options": generate_options(case["diagnosis"], case["distractors"]),
            "explanation": generate_explanation(case["diagnosis"], case["distractors"], case["concept"]),
            "trap_type": case["trap_type"], "tags": case["tags"],
        })
    
    return questions

# توليد كل الـ 12 ملف
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

print(f"\n🎉 Total: {total} questions across 12 subspecialties!")
