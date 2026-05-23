import os
import sys
import pandas as pd

# Thêm thư mục gốc vào đường dẫn hệ thống để fix triệt để lỗi ModuleNotFoundError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evaluate import danh_gia_va_luu_ket_qua
from src.preprocess_code import lam_sach_code

def jaccard_similarity(code1, code2, n=3):
    """Tính độ tương đồng Jaccard dựa trên Character N-grams"""
    # 1. Làm sạch code trước khi xử lý (Xóa comment, khoảng trắng thừa)
    code1_clean = lam_sach_code(str(code1) if pd.notna(code1) else "")
    code2_clean = lam_sach_code(str(code2) if pd.notna(code2) else "")
    
    # 2. Cắt N-grams
    ngrams1 = set([code1_clean[i:i+n] for i in range(len(code1_clean)-n+1)])
    ngrams2 = set([code2_clean[i:i+n] for i in range(len(code2_clean)-n+1)])
    
    intersection = ngrams1.intersection(ngrams2)
    union = ngrams1.union(ngrams2)
    
    if len(union) == 0: 
        return 0.0
        
    return len(intersection) / len(union)

def run_baseline_model(df):
    print("Đang chạy thuật toán Character N-grams + Jaccard Similarity trên dữ liệu đã làm sạch...")
    col1 = 'code_1_sach' if 'code_1_sach' in df.columns else 'File_1'
    col2 = 'code_2_sach' if 'code_2_sach' in df.columns else 'File_2'
    
    df['similarity_score'] = df.apply(lambda row: jaccard_similarity(row[col1], row[col2]), axis=1)
    return df

if __name__ == "__main__":
    print("--- BẮT ĐẦU CHẠY ĐÁNH GIÁ BASELINE ---")
    current_dir = os.path.dirname(__file__)
    # Chạy trên tập Test để đánh giá khách quan thay vì toàn bộ dữ liệu
    file_path = os.path.join(current_dir, '../data/processed/test_dataset.csv')
    thu_muc_luu = os.path.join(current_dir, 'results')
    
    try:
        df = pd.read_csv(file_path)
        df = run_baseline_model(df)
        
        y_true = df['Label'].values
        y_scores = df['similarity_score'].values
        file_pairs = (df['File_1'].astype(str) + " & " + df['File_2'].astype(str)) if 'File_1' in df.columns else ["Pair_" + str(i) for i in range(len(df))]
        
        danh_gia_va_luu_ket_qua(y_true=y_true, y_scores=y_scores, file_pairs=file_pairs, thu_muc_luu=thu_muc_luu)
        
    except FileNotFoundError:
        print(f"❌ Lỗi: Không tìm thấy file {file_path}. Vui lòng chạy file split_data.ipynb trước để tạo tập Test.")