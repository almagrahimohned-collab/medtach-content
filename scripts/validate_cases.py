#!/usr/bin/env python3
"""فحص جميع ملفات الحالات والتأكد من صحتها"""

import json
import os
from pathlib import Path
from collections import defaultdict

CASES_DIR = Path("../cases")
INDEX_FILE = Path("../index.json")

def check_json_file(filepath):
    """التحقق من صحة ملف JSON"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data, None
    except json.JSONDecodeError as e:
        return None, f"❌ Invalid JSON: {e}"
    except Exception as e:
        return None, f"❌ Error: {e}"

def validate_case(case_data, filepath):
    """التحقق من البيانات المطلوبة في الحالة"""
    errors = []
    required_fields = ['id', 'specialty', 'difficulty', 'title', 'chief_complaint', 
                       'correct_diagnosis', 'patient', 'hidden_data']
    
    for field in required_fields:
        if field not in case_data:
            errors.append(f"  ❌ Missing required field: '{field}'")
    
    if 'patient' in case_data:
        patient = case_data['patient']
        for pfield in ['age', 'gender', 'name']:
            if pfield not in patient:
                errors.append(f"  ❌ Missing patient field: '{pfield}'")
    
    return errors

def main():
    print("=" * 60)
    print("🔍 MedTach Case Validator")
    print("=" * 60)
    
    # 1. فحص index.json
    print("\n📋 Checking index.json...")
    index_data, index_error = check_json_file(INDEX_FILE)
    if index_error:
        print(f"  {index_error}")
        return
    print(f"  ✅ index.json loaded - {index_data['total_cases']} cases listed")
    
    # 2. فحص كل ملفات الحالات
    stats = defaultdict(lambda: defaultdict(int))
    errors_found = []
    missing_files = []
    
    print("\n📁 Checking case files...")
    for case in index_data['cases']:
        filepath = Path("..") / case['path']
        if not filepath.exists():
            missing_files.append(case['path'])
            errors_found.append(f"  ❌ Missing file: {case['path']}")
            continue
        
        data, error = check_json_file(filepath)
        if error:
            errors_found.append(f"  {case['path']}: {error}")
            continue
        
        case_errors = validate_case(data, filepath)
        if case_errors:
            errors_found.append(f"  ⚠️  {case['path']}:")
            errors_found.extend(case_errors)
        
        stats[case['specialty']][case['difficulty']] += 1
    
    # 3. فحص ملفات مش موجودة في الـ index
    print("\n📁 Checking for unindexed files...")
    all_case_files = set()
    for root, dirs, files in os.walk(CASES_DIR):
        for file in files:
            if file.endswith('.json'):
                rel_path = os.path.relpath(os.path.join(root, file), CASES_DIR)
                all_case_files.add("cases/" + rel_path)
    
    indexed_files = set(case['path'] for case in index_data['cases'])
    unindexed = all_case_files - indexed_files
    
    # 4. النتائج
    print("\n" + "=" * 60)
    print("📊 RESULTS")
    print("=" * 60)
    
    print(f"\n📈 Specialty Distribution:")
    for spec, diffs in sorted(stats.items()):
        total = sum(diffs.values())
        levels = ', '.join(f"{lvl}: {cnt}" for lvl, cnt in sorted(diffs.items()))
        print(f"  🏥 {spec}: {total} cases ({levels})")
    
    print(f"\n📁 Files:")
    print(f"  ✅ Indexed cases: {len(index_data['cases'])}")
    print(f"  ✅ Actual JSON files: {len(all_case_files)}")
    print(f"  ⚠️  Unindexed files: {len(unindexed)}")
    print(f"  ⚠️  Missing files: {len(missing_files)}")
    
    if unindexed:
        print(f"\n  Unindexed files (not in index.json):")
        for f in sorted(unindexed)[:10]:
            print(f"    📄 {f}")
        if len(unindexed) > 10:
            print(f"    ... and {len(unindexed) - 10} more")
    
    if missing_files:
        print(f"\n  Missing files (in index but not on disk):")
        for f in missing_files[:10]:
            print(f"    ❌ {f}")
        if len(missing_files) > 10:
            print(f"    ... and {len(missing_files) - 10} more")
    
    if errors_found:
        print(f"\n  ⚠️  Validation errors ({len(errors_found)}):")
        for err in errors_found[:15]:
            print(err)
        if len(errors_found) > 15:
            print(f"    ... and {len(errors_found) - 15} more errors")
    
    print("\n" + "=" * 60)
    if not errors_found and not missing_files:
        print("🎉 ALL CASES VALIDATED SUCCESSFULLY!")
    else:
        print(f"⚠️  Found {len(errors_found)} errors and {len(missing_files)} missing files")
    print("=" * 60)

if __name__ == "__main__":
    main()
