import os
import json
import re
import time
from pathlib import Path

def apply_test_improvements():
    """Apply generated test improvements"""
    try:
        if not os.path.exists('test_improvements.json'):
            print("File test_improvements.json tidak ditemukan")
            return 0
            
        with open('test_improvements.json', 'r') as f:
            improvements = json.load(f)
        
        if not improvements:
            print("Tidak ada perbaikan test yang ditemukan")
            return 0
        
        applied_count = 0
        for improvement in improvements:
            test_file = improvement.get('test_file')
            test_content = improvement.get('test_content')
            
            if not test_file or not test_content:
                continue
            
            # Pastikan direktori ada
            os.makedirs(os.path.dirname(test_file), exist_ok=True)
            
            # Tulis file test
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            applied_count += 1
            print(f"Membuat file test: {test_file}")
        
        return applied_count
    except Exception as e:
        print(f"Error menerapkan perbaikan test: {e}")
        return 0

def extract_code_from_markdown(text):
    """Extract code blocks from markdown text"""
    # Find Python code blocks
    code_pattern = re.compile(r'```python(.*?)```', re.DOTALL)
    code_match = code_pattern.search(text)
    if code_match:
        return code_match.group(1).strip()
    
    # Find generic code blocks
    generic_pattern = re.compile(r'```(.*?)```', re.DOTALL)
    generic_match = generic_pattern.search(text)
    if generic_match:
        return generic_match.group(1).strip()
    
    return text

def apply_code_fixes():
    """Apply generated code fixes"""
    try:
        if not os.path.exists('code_fixes.json'):
            print("File code_fixes.json tidak ditemukan")
            return 0
            
        with open('code_fixes.json', 'r') as f:
            fixes = json.load(f)
        
        if not fixes:
            print("Tidak ada perbaikan kode yang ditemukan")
            return 0
            
        applied_count = 0
        for fix in fixes:
            file_path = fix.get('file_path')
            fix_content = fix.get('fix_content')
            
            if not file_path or not fix_content:
                continue
            
            # Ekstrak kode dari respons markdown AI
            code_fix = extract_code_from_markdown(fix_content)
            
            # Cek apakah perbaikan berisi file lengkap atau hanya snippet
            if "```python" in fix_content and len(code_fix.splitlines()) > 5:
                # Asumsikan ini adalah penggantian file lengkap
                with open(file_path, 'w') as f:
                    f.write(code_fix)
                applied_count += 1
                print(f"Menerapkan perbaikan lengkap ke: {file_path}")
            else:
                # Untuk perbaikan snippet, kita memerlukan logika tambahan (sederhana)
                print(f"Perbaikan parsial untuk {file_path} - memerlukan tinjauan manual")
                with open(f"{file_path}.fix.txt", 'w') as f:
                    f.write(f"PERBAIKAN YANG DISARANKAN:\n\n{fix_content}")
                print(f"Sugesti perbaikan disimpan di: {file_path}.fix.txt")
        
        return applied_count
    except Exception as e:
        print(f"Error menerapkan perbaikan kode: {e}")
        return 0

def generate_improvement_report(test_count, fix_count):
    """Generate a report of improvements made"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    report = {
        "test_improvements": test_count,
        "code_fixes": fix_count,
        "timestamp": timestamp
    }
    
    with open('improvement_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Laporan perbaikan: {test_count} peningkatan test, {fix_count} perbaikan kode")

def main():
    """Main function to apply all improvements"""
    # Terapkan perbaikan test
    test_count = apply_test_improvements()
    print(f"Menerapkan {test_count} perbaikan test")
    
    # Terapkan perbaikan kode
    fix_count = apply_code_fixes()
    print(f"Menerapkan {fix_count} perbaikan kode")
    
    # Hasilkan laporan
    generate_improvement_report(test_count, fix_count)
    print("Proses penerapan perbaikan selesai!")

if __name__ == "__main__":
    main()