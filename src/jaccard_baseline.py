
"""
- Xây dựng thuật toán Baseline cho hệ thống phát hiện đạo văn.
    - Trích xuất đặc trưng bằng kỹ thuật Character N-grams (n=3).
    - Tính toán độ tương đồng giữa 2 đoạn code bằng Jaccard Similarity.
    - Áp dụng ngưỡng Threshold cố định (0.65) để phân loại nhãn (0: Tự làm, 1: Đạo văn).
"""



import pandas as pd

def jaccard_similarity(code1, code2, n=3):
    """
    Thuật toán tính độ tương đồng Jaccard dựa trên Character N-grams
    n=3: Cắt chuỗi thành các cụm 3 ký tự (3-grams)
    """
    # Tạo tập hợp các N-grams từ mã nguồn đã làm sạch
    ngrams1 = set([code1[i:i+n] for i in range(len(code1)-n+1)])
    ngrams2 = set([code2[i:i+n] for i in range(len(code2)-n+1)])
    
    # Tính phần Giao (Intersection) và phần Hợp (Union)
    intersection = ngrams1.intersection(ngrams2)
    union = ngrams1.union(ngrams2)
    
    # Tránh lỗi chia cho 0
    if len(union) == 0: 
        return 0.0
        
    return len(intersection) / len(union)

def run_baseline_model(df, threshold=0.65):
    """
    Hàm thực thi mô hình baseline trên toàn bộ dataframe
    """
    print("Đang chạy thuật toán Character N-grams + Jaccard Similarity...")
    
    # Tính điểm tương đồng cho tất cả các cặp bài
    df['similarity_score'] = df.apply(lambda row: jaccard_similarity(row['code_1_sach'], row['code_2_sach']), axis=1)
    
    # Áp dụng ngưỡng (Threshold) để dự đoán nhãn Đạo văn (1) hoặc Tự làm (0)
    df['du_doan'] = (df['similarity_score'] > threshold).astype(int)
    
    print(f"Hoàn tất: Đã chấm điểm và dán nhãn dự đoán với ngưỡng threshold = {threshold}")
    return df