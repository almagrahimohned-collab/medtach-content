#!/usr/bin/env python3
"""
🔥 Question Schema Migration v2
يحول الأسئلة من subject/topic → specialty/subspecialty/condition/concept
+ tags + cognitiveLevel + trapType
"""

import json, os
from pathlib import Path

QUESTIONS_DIR = Path("../questions")
INDEX_FILE = Path("../questions/index.json")

# 🧠 SPECIALTY MAPPING - القديم → الجديد
SPECIALTY_MAP = {
    'cardiology': {'specialty': 'internal_medicine', 'subspecialty': 'cardiology'},
    'pulmonology': {'specialty': 'internal_medicine', 'subspecialty': 'pulmonology'},
    'neurology': {'specialty': 'internal_medicine', 'subspecialty': 'neurology'},
    'endocrinology': {'specialty': 'internal_medicine', 'subspecialty': 'endocrinology'},
    'gastroenterology': {'specialty': 'internal_medicine', 'subspecialty': 'gastroenterology'},
    'nephrology': {'specialty': 'internal_medicine', 'subspecialty': 'nephrology'},
    'hematology': {'specialty': 'internal_medicine', 'subspecialty': 'hematology'},
    'infectious': {'specialty': 'internal_medicine', 'subspecialty': 'infectious_disease'},
    'rheumatology': {'specialty': 'internal_medicine', 'subspecialty': 'rheumatology'},
    'pediatrics': {'specialty': 'pediatrics', 'subspecialty': 'general_pediatrics'},
    'surgery': {'specialty': 'surgery', 'subspecialty': 'general_surgery'},
    'gynecology': {'specialty': 'obgyn', 'subspecialty': 'gynecology'},
    'obstetrics': {'specialty': 'obgyn', 'subspecialty': 'obstetrics'},
}

# 🎯 COGNITIVE LEVEL DETECTION من السؤال
def detect_cognitive_level(question_text, explanation, options):
    text = (question_text + ' ' + explanation).lower()
    
    if any(w in text for w in ['emergency', 'immediate', 'life-threatening', 'stat', 'urgent']):
        return 'emergency_reasoning'
    if any(w in text for w in ['management', 'treatment', 'next step', 'prescribe', 'therapy']):
        return 'decision_making'
    if any(w in text for w in ['ecg', 'x-ray', 'ct', 'mri', 'ultrasound', 'interpret', 'finding', 'image']):
        return 'interpretation'
    return 'recall'

# 🏷️ TAG DETECTION
def detect_tags(question_text, options, explanation):
    text = (question_text + ' ' + explanation).lower()
    tags = []
    
    if any(w in text for w in ['ecg', 'ekg', 'electrocardiogram', 'rhythm', 'st elevation']):
        tags.append('ecg')
    if any(w in text for w in ['x-ray', 'cxr', 'chest x', 'radiograph', 'imaging', 'ct', 'mri']):
        tags.append('imaging')
    if any(w in text for w in ['diagnosis', 'diagnose', 'identify', 'most likely']):
        tags.append('diagnosis')
    if any(w in text for w in ['management', 'treatment', 'therapy', 'medication', 'drug']):
        tags.append('treatment')
    if any(w in text for w in ['emergency', 'acute', 'urgent', 'stat', 'immediate']):
        tags.append('emergency')
    if any(w in text for w in ['pharmacology', 'drug', 'dose', 'side effect', 'interaction']):
        tags.append('pharmacology')
    if any(w in text for w in ['lab', 'laboratory', 'cbc', 'cmp', 'troponin', 'creatinine']):
        tags.append('laboratory')
    if any(w in text for w in ['prevention', 'vaccine', 'screening', 'prophylaxis']):
        tags.append('prevention')
    
    return tags if tags else ['diagnosis']

# ⚠️ TRAP TYPE DETECTION
def detect_trap_type(question_text, options, explanation):
    text = (question_text + ' ' + explanation).lower()
    
    if any(w in text for w in ['ecg', 'ekg', 'st elevation', 'rhythm', 'electrocardiogram']):
        return 'ecg_misread'
    if any(w in text for w in ['x-ray', 'cxr', 'imaging', 'radiograph', 'ct']):
        return 'imaging_misinterpretation'
    if any(w in text for w in ['lab', 'laboratory', 'troponin', 'creatinine', 'cbc']):
        return 'lab_misinterpretation'
    if any(w in text for w in ['similar', 'confused', 'mimic', 'differential']):
        return 'diagnostic_confusion'
    if any(w in text for w in ['dose', 'drug', 'interaction', 'side effect', 'contraindication']):
        return 'pharmacology_confusion'
    
    return 'diagnostic_confusion'

# 🎯 MIGRATE SINGLE QUESTION
def migrate_question(filepath):
    with open(filepath, 'r') as f:
        q = json.load(f)
    
    old_subject = q.get('subject', 'cardiology')
    mapping = SPECIALTY_MAP.get(old_subject, {'specialty': 'internal_medicine', 'subspecialty': old_subject})
    
    options = q.get('options', [])
    question_text = q.get('question', '')
    explanation = q.get('explanation', '')
    
    # Build new schema
    q['specialty'] = mapping['specialty']
    q['subspecialty'] = mapping['subspecialty']
    q['condition'] = q.get('topic', q.get('title', ''))
    q['concept'] = q.get('title', '')
    
    # New fields
    q['cognitive_level'] = detect_cognitive_level(question_text, explanation, options)
    q['tags'] = detect_tags(question_text, options, explanation)
    q['trap_type'] = detect_trap_type(question_text, options, explanation)
    q['learning_objective'] = f"Master {q.get('title', 'this concept')} in {mapping['subspecialty']}"
    q['difficulty_weight'] = {'beginner': 1, 'intermediate': 2, 'advanced': 3}.get(q.get('difficulty', 'beginner'), 1)
    
    with open(filepath, 'w') as f:
        json.dump(q, f, indent=2)
    
    return q

# 📊 MIGRATE ALL
def migrate_all():
    if not INDEX_FILE.exists():
        print("❌ index.json not found")
        return
    
    with open(INDEX_FILE, 'r') as f:
        index = json.load(f)
    
    questions = index.get('questions', [])
    stats = {'migrated': 0, 'errors': 0, 'specialties': {}}
    
    for q_entry in questions:
        filepath = Path("..") / q_entry["path"]
        if not filepath.exists():
            stats['errors'] += 1
            continue
        
        try:
            q = migrate_question(filepath)
            q_entry['specialty'] = q['specialty']
            q_entry['subspecialty'] = q['subspecialty']
            q_entry['condition'] = q.get('condition', '')
            q_entry['tags'] = q.get('tags', [])
            q_entry['cognitive_level'] = q.get('cognitive_level', 'recall')
            
            spec = q['specialty']
            if spec not in stats['specialties']:
                stats['specialties'][spec] = 0
            stats['specialties'][spec] += 1
            
            stats['migrated'] += 1
            print(f"  ✅ {q.get('title', filepath.name)}")
        except Exception as e:
            stats['errors'] += 1
            print(f"  ❌ {filepath}: {e}")
    
    # Update index
    index['version'] = '2.0'
    index['schema'] = 'specialty/subspecialty/condition/concept'
    
    # Build subjects summary
    subjects = {}
    for q in questions:
        spec = q.get('specialty', 'internal_medicine')
        sub = q.get('subspecialty', '')
        if spec not in subjects:
            subjects[spec] = {'count': 0, 'subspecialties': {}}
        subjects[spec]['count'] += 1
        if sub not in subjects[spec]['subspecialties']:
            subjects[spec]['subspecialties'][sub] = 0
        subjects[spec]['subspecialties'][sub] += 1
    
    index['subjects'] = subjects
    index['total_questions'] = stats['migrated']
    
    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, indent=2)
    
    print(f"\n🎉 Migration Complete!")
    print(f"📊 Migrated: {stats['migrated']} | Errors: {stats['errors']}")
    print(f"🏥 Specialties:")
    for spec, count in sorted(stats['specialties'].items()):
        print(f"  {spec}: {count} questions")

if __name__ == "__main__":
    migrate_all()
