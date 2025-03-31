import os
import json
import glob
import openai
import re
from pathlib import Path

# Setup SambaNova client
client = openai.OpenAI(
    api_key=os.environ.get("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

def load_sonarqube_issues():
    """Load SonarQube issues from the exported JSON"""
    with open('sonar_issues.json', 'r') as f:
        return json.load(f)

def load_coverage_data():
    """Load code coverage data from SonarQube"""
    with open('code_coverage.json', 'r') as f:
        return json.load(f)

def get_file_content(file_path):
    """Get content of a file"""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def find_files_needing_tests():
    """Find files with low test coverage"""
    # Untuk demonstrasi, kita cari file Python tanpa file test terkait
    uncovered_files = []
    
    # Temukan file Python
    python_files = glob.glob('**/*.py', recursive=True)
    for file in python_files:
        # Lewati file test dan file di virtual environment
        if 'test' in file.lower() or file.startswith('venv/'):
            continue
        # Periksa apakah ada file test terkait
        test_file = f"tests/test_{os.path.basename(file)}"
        if not os.path.exists(test_file):
            uncovered_files.append(file)
    
    return uncovered_files

def generate_test_case(file_path):
    """Generate test case for a file using SambaNova GenAI"""
    content = get_file_content(file_path)
    if not content:
        return None
    
    # Prepare prompt for test generation
    prompt = f"""
    Anda adalah asisten yang membuat test case berkualitas tinggi.
    
    File berikut membutuhkan test case:
    
    ```python
    {content}
    ```
    
    Hasilkan tes pytest yang komprehensif dan berkualitas tinggi untuk file ini. Tes harus:
    1. Mencakup semua fungsi dan metode
    2. Mencakup kasus normal dan edge cases
    3. Menggunakan mocking untuk dependensi eksternal
    4. Memiliki dokumentasi yang jelas
    5. Mengikuti praktik terbaik pytest
    
    Berikan kode test case lengkap yang siap dijalankan.
    """
    
    try:
        response = client.chat.completions.create(
            model="Qwen2.5-Coder-32B-Instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who writes high-quality test cases."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            top_p=0.1
        )
        
        test_content = response.choices[0].message.content
        
        # Extract code from markdown if needed
        code_pattern = re.compile(r'```python(.*?)```', re.DOTALL)
        code_match = code_pattern.search(test_content)
        if code_match:
            return code_match.group(1).strip()
        return test_content
    except Exception as e:
        print(f"Error generating test for {file_path}: {e}")
        return None

def fix_code_issue(issue):
    """Generate fix for a code issue using SambaNova GenAI"""
    file_path = issue.get('component').split(':')[-1]
    content = get_file_content(file_path)
    if not content:
        return None
    
    # Prepare prompt for code fix
    prompt = f"""
    Anda adalah asisten yang memperbaiki masalah kode.
    
    Ada masalah dalam file berikut:
    
    ```python
    {content}
    ```
    
    Masalah yang dilaporkan SonarQube:
    - Rule: {issue.get('rule')}
    - Pesan: {issue.get('message')}
    - Line: {issue.get('line', 'Not specified')}
    
    Berikan solusi untuk masalah ini dengan memperbaiki kode. Jelaskan apa yang Anda perbaiki dan mengapa.
    """
    
    try:
        response = client.chat.completions.create(
            model="Qwen2.5-Coder-32B-Instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who fixes code issues."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            top_p=0.1
        )
        
        fix_content = response.choices[0].message.content
        
        return {
            "file_path": file_path,
            "original_issue": issue,
            "fix_content": fix_content
        }
    except Exception as e:
        print(f"Error generating fix for issue in {file_path}: {e}")
        return None

def main():
    """Main function to orchestrate the improvement process"""
    # Buat direktori tests jika belum ada
    os.makedirs('tests', exist_ok=True)

    # Process test coverage improvements
    print("Mencari file yang membutuhkan test case...")
    uncovered_files = find_files_needing_tests()
    print(f"Menemukan {len(uncovered_files)} file yang membutuhkan test")
    
    test_improvements = []
    # Batasi ke 3 file saja untuk demonstrasi
    for file in uncovered_files[:3]:
        print(f"Menghasilkan test untuk {file}")
        test_content = generate_test_case(file)
        if test_content:
            test_file_path = f"tests/test_{os.path.basename(file)}"
            test_improvements.append({
                "original_file": file,
                "test_file": test_file_path,
                "test_content": test_content
            })
    
    # Simpan perbaikan test untuk diproses nanti
    with open('test_improvements.json', 'w') as f:
        json.dump(test_improvements, f, indent=2)
    
    print(f"Berhasil menghasilkan {len(test_improvements)} test case improvements")
    
    # Contoh membaca masalah SonarQube jika file ada
    if os.path.exists('sonar_issues.json'):
        issues = load_sonarqube_issues().get('issues', [])
        print(f"Menemukan {len(issues)} masalah kode untuk diperbaiki")
        
        code_fixes = []
        # Batasi ke 5 masalah saja untuk demonstrasi
        for issue in issues[:5]:
            print(f"Menghasilkan perbaikan untuk masalah: {issue.get('rule')}")
            fix = fix_code_issue(issue)
            if fix:
                code_fixes.append(fix)
        
        # Simpan perbaikan kode untuk diproses nanti
        with open('code_fixes.json', 'w') as f:
            json.dump(code_fixes, f, indent=2)
        
        print(f"Berhasil menghasilkan {len(code_fixes)} perbaikan kode")
    else:
        print("File sonar_issues.json tidak ditemukan. Melewati perbaikan kode")

if __name__ == "__main__":
    main()