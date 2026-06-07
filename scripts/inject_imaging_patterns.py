#!/usr/bin/env python3
"""🔥 Imaging Pattern Injector v3 - Smart Rule Engine + Confidence + Fallback"""

import json, os, re
from pathlib import Path

CASES_DIR = Path("../cases")
INDEX_FILE = Path("../index.json")

# 🧠 SMART RULE ENGINE - مع priorities + word boundaries
KEYWORD_MAP = {
    "cxr": {
        "pneumonia": {
            "keywords": ["pneumonia", "consolidation", "lobar pneumonia", "bronchopneumonia",
                        "tb", "tuberculosis", "bronchiectasis", "cystic fibrosis",
                        "lung abscess", "empyema"],
            "priority": 10,
            "require_boundary": True  # منع false match
        },
        "effusion": {
            "keywords": ["pleural effusion", "effusion", "pleural fluid", "hydrothorax",
                        "hemothorax", "empyema"],
            "priority": 8,
        },
        "pneumothorax": {
            "keywords": ["pneumothorax", "collapsed lung", "air leak", "tension pneumothorax"],
            "priority": 9,
        },
        "cardiomegaly": {
            "keywords": ["heart failure", "chf", "cardiomyopathy", "dilated cardiomyopathy",
                        "cardiomegaly", "enlarged heart", "pulmonary edema", "congestive heart"],
            "priority": 8,
        },
        "atelectasis": {
            "keywords": ["atelectasis", "lung collapse"],
            "priority": 6,
        },
    },
    "ct_brain": {
        "stroke": {
            "keywords": ["stroke", "cva", "ischemia", "infarction", "tia",
                        "cerebrovascular", "lacunar infarct"],
            "priority": 10,
            "exclude": ["heat stroke", "heatstroke"]  # منع false match
        },
        "hemorrhage": {
            "keywords": ["hemorrhage", "bleed", "hematoma", "ich", "sah",
                        "subarachnoid", "subdural", "epidural", "hemorrhagic stroke"],
            "priority": 10,
        },
        "tumor": {
            "keywords": ["brain tumor", "brain mass", "glioma", "meningioma",
                        "metastasis", "glioblastoma", "astrocytoma", "brain cancer"],
            "priority": 8,
        },
    },
    "us_abd": {
        "gallstones": {
            "keywords": ["gallstone", "cholelithiasis", "biliary colic", "cholecystitis"],
            "priority": 9,
        },
        "appendicitis": {
            "keywords": ["appendicitis", "appendix", "appendiceal"],
            "priority": 9,
        },
    },
    "ct_chest": {
        "pe": {
            "keywords": ["pulmonary embolism", "pe", "pulmonary embolus"],
            "priority": 10,
        },
        "mass": {
            "keywords": ["lung mass", "lung tumor", "lung cancer", "pulmonary nodule"],
            "priority": 8,
        },
    },
}

def smart_match(diagnosis, pattern_config):
    """بحث ذكي مع scoring"""
    if not diagnosis:
        return None, 0
    
    dx = diagnosis.lower().strip()
    keywords = pattern_config.get("keywords", [])
    priority = pattern_config.get("priority", 5)
    
    # منع false match
    if "exclude" in pattern_config:
        for excl in pattern_config["exclude"]:
            if excl.lower() in dx:
                return None, 0
    
    matched_keywords = []
    for kw in keywords:
        kw_lower = kw.lower()
        if pattern_config.get("require_boundary"):
            # استخدام word boundary لمنع false match
            if re.search(r'\b' + re.escape(kw_lower) + r'\b', dx):
                matched_keywords.append(kw)
        else:
            if kw_lower in dx:
                matched_keywords.append(kw)
    
    if not matched_keywords:
        return None, 0
    
    # Score = عدد الكلمات المتطابقة × priority
    score = len(matched_keywords) * priority
    # تطبيع score إلى 0-1
    confidence = min(score / 30, 0.95)
    
    return matched_keywords[0], confidence

def find_best_pattern(diagnosis, modality_rules):
    """أفضل pattern للتشخيص"""
    best_pattern = None
    best_score = 0
    best_confidence = 0
    
    for pattern_name, pattern_config in modality_rules.items():
        matched_kw, confidence = smart_match(diagnosis, pattern_config)
        if matched_kw and confidence > best_score:
            best_pattern = pattern_name
            best_score = confidence
            best_confidence = confidence
    
    return best_pattern, best_confidence

def inject_patterns():
    """حقن imaging_patterns مع confidence score"""
    
    with open(INDEX_FILE, 'r') as f:
        index = json.load(f)
    
    stats = {"total": len(index['cases']), "updated": 0, "skipped": 0,
             "patterns": {}, "fallbacks": 0}
    
    for case in index['cases']:
        filepath = CASES_DIR / case['path']
        if not filepath.exists():
            stats['skipped'] += 1
            continue
        
        with open(filepath, 'r') as f:
            case_data = json.load(f)
        
        diagnosis = case_data.get('correct_diagnosis', '') or case_data.get('title', '')
        chief = case_data.get('chief_complaint', '')
        
        # Initialize
        if 'imaging_patterns' not in case_data:
            case_data['imaging_patterns'] = {}
        
        modified = False
        
        for modality, rules in KEYWORD_MAP.items():
            # Skip if already has pattern (don't override)
            if modality in case_data.get('imaging_patterns', {}):
                continue
            
            pattern, confidence = find_best_pattern(diagnosis, rules)
            
            if pattern:
                case_data['imaging_patterns'][modality] = {
                    "pattern": pattern,
                    "confidence": round(confidence, 2),
                    "source": "rule_engine_v3"
                }
                stats['patterns'][modality] = stats['patterns'].get(modality, 0) + 1
                modified = True
            else:
                # ✅ Fallback
                case_data['imaging_patterns'][modality] = {
                    "pattern": "normal",
                    "confidence": 0.3,
                    "source": "fallback"
                }
                stats['fallbacks'] += 1
                modified = True
        
        if modified:
            with open(filepath, 'w') as f:
                json.dump(case_data, f, indent=2)
            stats['updated'] += 1
            print(f"  ✅ {case_data['title'][:40]}: {case_data['imaging_patterns']}")
    
    # 📊 نتائج
    print("\n" + "="*50)
    print("📊 INJECTION RESULTS (Smart Engine v3)")
    print("="*50)
    print(f"📁 Total: {stats['total']} | ✅ Updated: {stats['updated']} | ⏭️ Skipped: {stats['skipped']}")
    print(f"🔄 Fallbacks (normal): {stats['fallbacks']}")
    print(f"\n📋 Patterns by modality:")
    for mod, count in sorted(stats.get('patterns', {}).items()):
        print(f"  {mod}: {count} patterns")
    
    # Rebuild index
    print("\n📋 Rebuilding index.json...")
    os.system("cd .. && ./build_index.sh > index.json 2>/dev/null")
    print("✅ Done!")

if __name__ == "__main__":
    inject_patterns()
