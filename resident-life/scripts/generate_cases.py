#!/usr/bin/env python3
"""
Resident Life Case Generator
Generates patient cases for Resident Life simulator from medtach-content
Uses existing questions, cases, and diagnoses to create realistic clinical scenarios
"""

import json
import os
import random
import re
from pathlib import Path

class ResidentCaseGenerator:
    def __init__(self, content_path=None):
        if content_path is None:
            self.content_path = Path(os.path.expanduser("~/medtach-content"))
        else:
            self.content_path = Path(content_path)
        self.diagnoses = self._load_diagnoses()
        
    def _load_diagnoses(self):
        """Load diagnoses from diagnoses.txt"""
        diagnoses_file = self.content_path / "diagnoses.txt"
        if diagnoses_file.exists():
            with open(diagnoses_file, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        return []
    
    def _generate_name(self):
        """Generate a realistic name"""
        first_names_male = ["Ahmed", "Hassan", "Omar", "Khalid", "Ibrahim", "Youssef", "Ali", "Mustafa", "Tariq", "Bilal"]
        first_names_female = ["Fatima", "Layla", "Samira", "Nour", "Aisha", "Mariam", "Zainab", "Huda", "Amal", "Sara"]
        last_names = ["Al-Rashid", "Al-Farsi", "Al-Hashimi", "Al-Qassim", "Al-Sayed", "Khan", "Malik", "Ahmed", "Hassan", "Omar"]
        
        if random.choice([True, False]):
            return f"{random.choice(first_names_male)} {random.choice(last_names)}"
        else:
            return f"{random.choice(first_names_female)} {random.choice(last_names)}"
    
    def _extract_age(self, text):
        """Extract age from question text"""
        match = re.search(r'(\d+)[-\s]year[-\s]old', text)
        if match:
            return int(match.group(1))
        return random.randint(25, 75)
    
    def _extract_gender(self, text):
        """Extract gender from question text"""
        if any(word in text.lower() for word in ['woman', 'female', 'she', 'lady', 'girl', 'mother', 'sister']):
            return 'female'
        return 'male'
    
    def _extract_complaint(self, text):
        """Extract chief complaint"""
        if 'presents with' in text:
            parts = text.split('presents with')
            if len(parts) > 1:
                complaint = parts[1].split('.')[0].strip()
                if len(complaint) > 150:
                    return complaint[:147] + "..."
                return complaint
        # Try to get first sentence
        sentences = text.split('. ')
        if len(sentences) > 0:
            return sentences[0][:150]
        return text[:150]
    
    def _determine_triage(self, q):
        """Determine triage level"""
        text = q.get('question', '').lower()
        topic = q.get('topic', '').lower()
        condition = q.get('condition', '').lower()
        
        critical_keywords = ['stemi', 'cardiac arrest', 'tamponade', 'dissection', 'stroke', 'code',
                            'massive', 'rupture', 'airway', 'anaphylaxis', 'shock']
        urgent_keywords = ['nstemi', 'heart failure', 'pneumonia', 'sepsis', 'dka', 'fracture',
                          'bleeding', 'syncope', 'chest pain', 'sob']
        
        all_text = text + " " + topic + " " + condition
        
        if any(kw in all_text for kw in critical_keywords):
            return 1
        if any(kw in all_text for kw in urgent_keywords):
            return 2
        return 3
    
    def _generate_actions_from_question(self, q):
        """Generate possible actions based on question"""
        text = q.get('question', '').lower()
        actions = []
        
        # Always include ECG for cardiac
        if 'cardio' in q.get('subject', '').lower() or 'cardio' in q.get('system', '').lower():
            actions.append({
                "id": "ecg", "name": "12-Lead ECG", "category": "investigation",
                "timeCost": 8, "resultTime": 0, "isEssential": True,
                "result": {"finding": "ECG findings (see description)", "interpretation": "Interpret based on clinical context"}
            })
        
        # Include labs based on keywords
        if any(w in text for w in ['fever', 'infection', 'sepsis', 'pneumonia']):
            actions.append({
                "id": "cbc", "name": "CBC", "category": "lab",
                "timeCost": 5, "resultTime": 20, "isEssential": True,
                "result": {"finding": "WBC 15.2, Hb 13.5, Plt 220", "interpretation": "Leukocytosis suggests infection"}
            })
            actions.append({
                "id": "crp", "name": "CRP", "category": "lab",
                "timeCost": 5, "resultTime": 25, "isEssential": False,
                "result": {"finding": "CRP: 85 mg/L", "interpretation": "Elevated - suggests bacterial infection"}
            })
        
        if any(w in text for w in ['chest pain', 'cardiac', 'mi', 'heart']):
            actions.append({
                "id": "troponin", "name": "High-Sensitivity Troponin I", "category": "lab",
                "timeCost": 5, "resultTime": 25, "isEssential": True,
                "result": {"finding": "hs-cTnI: pending", "interpretation": "Check serial troponins"}
            })
        
        if any(w in text for w in ['x-ray', 'cxr', 'chest xray', 'pulmonary', 'lung', 'pneumonia', 'sob', 'dyspnea']):
            actions.append({
                "id": "cxr", "name": "Chest X-Ray", "category": "imaging",
                "timeCost": 12, "resultTime": 15, "isEssential": False,
                "result": {"finding": "CXR findings pending", "interpretation": "Awaiting radiology read"}
            })
        
        if any(w in text for w in ['ct', 'trauma', 'dissection', 'stroke', 'head']):
            actions.append({
                "id": "ct_scan", "name": "CT Scan", "category": "imaging",
                "timeCost": 20, "resultTime": 25, "isEssential": False,
                "result": {"finding": "CT findings pending", "interpretation": "Awaiting radiology read"}
            })
        
        # Ensure at least 4 actions
        if len(actions) < 4:
            actions.append({
                "id": "history", "name": "Detailed History", "category": "clinical",
                "timeCost": 8, "resultTime": 0, "isEssential": True,
                "result": {"finding": "History obtained", "interpretation": "Key clinical information gathered"}
            })
            actions.append({
                "id": "exam", "name": "Physical Examination", "category": "clinical",
                "timeCost": 5, "resultTime": 0, "isEssential": True,
                "result": {"finding": "Examination completed", "interpretation": "Physical findings documented"}
            })
        
        return actions[:8]  # Max 8 actions
    
    def generate_case_from_question(self, question_data):
        """Convert a medtach question into a Resident Life patient case"""
        q = question_data
        
        patient = {
            "id": f"gen_{q.get('id', 'unknown')}",
            "name": self._generate_name(),
            "age": self._extract_age(q.get('question', '')),
            "gender": self._extract_gender(q.get('question', '')),
            "complaint": self._extract_complaint(q.get('question', '')),
            "triageNote": f"Generated case - {q.get('topic', 'general')}",
            "correctTriage": self._determine_triage(q),
            "correctDiagnosis": q.get('condition', 'Unknown'),
            "differentialDiagnoses": [
                opt.get('text', '') for opt in q.get('options', []) 
                if not opt.get('isCorrect', False)
            ][:4],
            "possibleActions": self._generate_actions_from_question(q),
            "treatmentPathway": {
                "correct": [a['id'] for a in self._generate_actions_from_question(q) if a.get('isEssential')],
                "acceptable": [a['id'] for a in self._generate_actions_from_question(q)],
                "wrongActions": [],
                "wrongActionsConsequence": "Inappropriate management may lead to clinical deterioration",
                "criticalErrors": []
            },
            "deteriorationPattern": {
                "withoutTreatment": {
                    "timer": 30,
                    "stages": [
                        {"time": 10, "event": "Clinical deterioration beginning"},
                        {"time": 20, "event": "Critical condition developing"},
                        {"time": 30, "event": "Life-threatening if no intervention"}
                    ]
                },
                "withCorrectTreatment": {
                    "timer": 120,
                    "stages": [
                        {"time": 30, "event": "Clinical improvement noted"},
                        {"time": 60, "event": "Patient stabilizing"},
                        {"time": 120, "event": "Patient stable, plan for disposition"}
                    ]
                }
            },
            "learningPoints": {
                "missedDiagnosis": f"Consider differential diagnoses: {', '.join([opt.get('text', '') for opt in q.get('options', []) if not opt.get('isCorrect', False)][:3])}",
                "keyTeaching": q.get('keyTakeaway', 'No specific teaching point'),
                "guideline": q.get('references', ['No specific guideline'])[0] if q.get('references') else 'Standard clinical practice'
            },
            "difficulty": q.get('difficulty', 'beginner'),
            "xpReward": {"beginner": 100, "intermediate": 200, "advanced": 350}.get(q.get('difficulty', 'beginner'), 100),
            "reputationImpact": {
                "correctDiagnosis": 20,
                "correctTreatment": 30,
                "missedDiagnosis": -40,
                "patientDeath": -80
            }
        }
        
        return patient
    
    def generate_from_file(self, question_file):
        """Generate a case from a question JSON file"""
        with open(question_file, 'r') as f:
            q = json.load(f)
        return self.generate_case_from_question(q)
    
    def generate_batch_from_directory(self, specialty_dir, output_file):
        """Generate multiple cases from a question directory"""
        cases = []
        question_dir = self.content_path / "questions" / specialty_dir
        
        if not question_dir.exists():
            print(f"❌ Directory not found: {question_dir}")
            return None
        
        # Get JSON files
        json_files = list(question_dir.glob("*.json"))
        
        # Check subdirectories too
        for subdir in question_dir.glob("*/"):
            json_files.extend(subdir.glob("*.json"))
        
        for q_file in json_files:
            if q_file.name == "index.json":
                continue
            try:
                case = self.generate_from_file(str(q_file))
                cases.append(case)
                print(f"  ✅ Generated: {case['name']} - {case['correctDiagnosis'][:60]}")
            except Exception as e:
                print(f"  ❌ Error processing {q_file.name}: {e}")
        
        if not cases:
            print(f"⚠️  No cases generated for {specialty_dir}")
            return None
        
        # Save to output file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        result = {
            "module": "resident-life",
            "category": specialty_dir,
            "version": "1.0",
            "description": f"Clinical cases for {specialty_dir} - generated from medtach-content questions",
            "patients": cases,
            "metadata": {
                "totalCases": len(cases),
                "source": f"Generated from questions/{specialty_dir}",
                "generatedBy": "generate_cases.py",
                "difficultyRange": f"{min(c['difficulty'] for c in cases)} to {max(c['difficulty'] for c in cases)}"
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Generated {len(cases)} cases → {output_file}")
        return result


def main():
    print("=" * 60)
    print("🏥 Resident Life Case Generator")
    print("=" * 60)
    print()
    
    generator = ResidentCaseGenerator()
    
    print(f"📚 Loaded {len(generator.diagnoses)} diagnoses from database")
    print()
    
    # Generate from all available specialties
    specialties_dir = generator.content_path / "questions"
    
    if not specialties_dir.exists():
        print("❌ questions/ directory not found!")
        return
    
    specialties = [d.name for d in specialties_dir.iterdir() if d.is_dir()]
    
    print(f"📁 Found specialties: {', '.join(specialties)}")
    print()
    
    for specialty in specialties:
        print(f"🔄 Generating {specialty} cases...")
        output = generator.content_path / "resident-life" / "patients" / f"{specialty}_generated.json"
        generator.generate_batch_from_directory(specialty, str(output))
        print()
    
    print("=" * 60)
    print("✅ All cases generated successfully!")
    print(f"📁 Output: {generator.content_path}/resident-life/patients/")
    print("=" * 60)


if __name__ == "__main__":
    main()
