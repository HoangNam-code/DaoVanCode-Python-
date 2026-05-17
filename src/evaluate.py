import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix

def danh_gia_va_luu_ket_qua(y_true, y_pred, thu_muc_luu="src/results"):
    """
    Hàm tính toán các metric, vẽ Confusion Matrix và lưu file tự động.
    """
    # Tạo thư mục results nếu chưa có
    if not os.path.exists(thu_muc_luu):
        os.makedirs(thu_muc_luu)

    print("Đang tiến hành đánh giá mô hình...")

    # ==========================================
    # 1. TẠO VÀ LƯU BẢNG METRIC (.csv và .txt)
    # ==========================================
    # Lưu dạng file CSV để làm minh chứng Bảng Metric
    report_dict = classification_report(y_true, y_pred, output_dict=True)
    df_metrics = pd.DataFrame(report_dict).transpose()
    csv_path = os.path.join(thu_muc_luu, "bang_metric.csv")
    df_metrics.to_csv(csv_path)

    # Lưu dạng Text để dễ đọc
    report_text = classification_report(y_true, y_pred, target_names=['Tự làm (0)', 'Đạo văn (1)'])
    txt_path = os.path.join(thu_muc_luu, "nhan_xet_metric.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("BẢNG ĐÁNH GIÁ METRIC (Precision, Recall, F1-Score)\n")
        f.write("="*50 + "\n")
        f.write(report_text)

    # ==========================================
    # 2. VẼ VÀ LƯU CONFUSION MATRIX (.png)
    # ==========================================
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    
    # Thiết kế biểu đồ
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Dự đoán: Tự làm (0)', 'Dự đoán: Đạo văn (1)'], 
                yticklabels=['Thực tế: Tự làm (0)', 'Thực tế: Đạo văn (1)'],
                annot_kws={"size": 14}) # Phóng to số trong ô
    
    plt.title('Ma trận nhầm lẫn (Confusion Matrix)', fontsize=14, pad=15)
    plt.tight_layout()

    # Lưu file ảnh
    png_path = os.path.join(thu_muc_luu, "confusion_matrix.png")
    plt.savefig(png_path, dpi=300) # dpi=300 để ảnh nét khi đưa vào Word
    plt.close()

    print(f"✅ HOÀN TẤT! Đã lưu các file minh chứng vào thư mục: '{thu_muc_luu}'")
    print(f" - {csv_path}")
    print(f" - {txt_path}")
    print(f" - {png_path}")

# ==========================================
# KHỐI CODE ĐỂ BẠN TỰ TEST ĐỘC LẬP
# ==========================================
if __name__ == "__main__":
    # Đây là dữ liệu giả lập để bạn test xem code chạy tạo file được chưa.
    # Trong thực tế, bạn sẽ import hàm này vào file chạy chính và truyền 
    # df['Label'] và df['du_doan'] từ file của bạn Hòa vào đây.
    
    nhan_thuc_te = [0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0]
    nhan_du_doan = [0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0]
    
    danh_gia_va_luu_ket_qua(nhan_thuc_te, nhan_du_doan)