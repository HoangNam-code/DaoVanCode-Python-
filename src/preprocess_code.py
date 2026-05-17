"""Đọc dữ liệu mã nguồn gốc từ thư mục raw.
    - Tiền xử lý (Preprocessing): Dùng Regex để xóa bình luận (comments), 
      xóa docstrings và chuẩn hóa khoảng trắng.
    - Trả về các đoạn mã nguồn đã được làm sạch để phục vụ bước trích xuất đặc trưng.
"""

import pandas as pd
import os
import re

def get_base_dir():
    path_mac = '/Users/hoangvuhoa/Desktop/DaoVanCode/data/processed/archive'
    path_relative = 'data/processed/archive'
    
    if os.path.exists(path_mac):
        return path_mac
    return path_relative

def doc_noi_dung(base_dir, ten_file):
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
    # Xóa comment đơn dòng bắt đầu bằng dấu #
    code_text = re.sub(r'#.*', '', code_text)
    # Xóa chú thích đa dòng (docstrings)
    code_text = re.sub(r'(\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\")', '', code_text, flags=re.DOTALL)
    # Chuẩn hóa khoảng trắng dư thừa
    code_text = re.sub(r'\s+', ' ', code_text).strip()
    return code_text

if __name__ == "__main__":
    base_dir = get_base_dir()
    csv_path = os.path.join(base_dir, 'cheating_dataset.csv')
    
    print(f"Đang tiến hành đọc dữ liệu từ: {csv_path}")
    df = pd.read_csv(csv_path)
    
    print("Đang tiến hành làm sạch mã nguồn...")
    df['code_1_sach'] = df['File_1'].apply(lambda x: lam_sach_code(doc_noi_dung(base_dir, x)))
    df['code_2_sach'] = df['File_2'].apply(lambda x: lam_sach_code(doc_noi_dung(base_dir, x)))
    
    print("Hoàn tất: Dữ liệu đã được làm sạch và sẵn sàng để trích xuất đặc trưng!")