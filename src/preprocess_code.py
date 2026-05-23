import os
import re

def get_base_dir():
    """Lấy đường dẫn tương đối tự động tương thích mọi máy"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, '../data/raw/archive')

def doc_noi_dung(base_dir, ten_file):
    if pd.isna(ten_file): return ""
    if not str(ten_file).endswith('.py'):
        ten_file = str(ten_file) + '.py'
        
    duong_dan = os.path.join(base_dir, ten_file)
    try:
        with open(duong_dan, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def lam_sach_code(code_text):
    """Tiền xử lý: Xóa comment, docstring và chuẩn hóa khoảng trắng"""
    code_text = re.sub(r'#.*', '', str(code_text))
    code_text = re.sub(r"('''([\s\S]*?)'''|\"\"\"([\s\S]*?)\"\"\")", '', code_text)
    code_text = re.sub(r'\s+', ' ', code_text).strip()
    return code_text