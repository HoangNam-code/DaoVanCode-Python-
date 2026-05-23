import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import precision_recall_curve, classification_report, confusion_matrix

def danh_gia_va_luu_ket_qua(y_true, y_scores, file_pairs=None, thu_muc_luu="src/results"):
    """
    Hàm tối ưu threshold, tính toán metric, vẽ PR Curve, Confusion Matrix và phân tích FP/FN.
    """
    if not os.path.exists(thu_muc_luu):
        os.makedirs(thu_muc_luu)

    print("Đang tiến hành tối ưu ngưỡng, đánh giá mô hình và phân tích lỗi...")

    # 1. TRỰC QUAN HÓA PR CURVE VÀ TỐI ƯU THRESHOLD
    precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
    f1_scores = np.divide(2 * (precision * recall), (precision + recall), out=np.zeros_like(precision), where=(precision + recall) != 0)
    
    optimal_idx = np.argmax(f1_scores)
    optimal_threshold = thresholds[optimal_idx] if optimal_idx < len(thresholds) else thresholds[-1]
    
    print(f"\n--- KẾT QUẢ TỐI ƯU THRESHOLD ---")
    print(f"Ngưỡng (Threshold) tối ưu: {optimal_threshold:.4f}")
    print(f"F1-score cao nhất đạt được: {f1_scores[optimal_idx]:.4f}\n")

    plt.figure(figsize=(8, 6))
    plt.plot(recall, precision, marker='.', label='PR Curve', color='b')
    plt.scatter(recall[optimal_idx], precision[optimal_idx], color='red', zorder=5, label=f'Điểm tối ưu (Threshold = {optimal_threshold:.2f})')
    plt.title('Đồ thị Precision-Recall Curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.legend()
    plt.grid(True)
    pr_curve_path = os.path.join(thu_muc_luu, 'pr_curve.png')
    plt.savefig(pr_curve_path, dpi=300)
    plt.close()

    # 2. ĐÁNH GIÁ METRIC VÀ VẼ CONFUSION MATRIX
    y_pred = (y_scores >= optimal_threshold).astype(int)

    report_dict = classification_report(y_true, y_pred, output_dict=True)
    pd.DataFrame(report_dict).transpose().to_csv(os.path.join(thu_muc_luu, "bang_metric.csv"))

    report_text = classification_report(y_true, y_pred, target_names=['Tự làm (0)', 'Đạo văn (1)'])
    with open(os.path.join(thu_muc_luu, "nhan_xet_metric.txt"), "w", encoding="utf-8") as f:
        f.write(f"NGƯỠNG TỐI ƯU ĐƯỢC CHỌN: {optimal_threshold:.4f}\n")
        f.write("="*50 + "\n")
        f.write("BẢNG ĐÁNH GIÁ METRIC (Precision, Recall, F1-Score)\n")
        f.write("="*50 + "\n")
        f.write(report_text)

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Dự đoán: 0 (Tự làm)', 'Dự đoán: 1 (Đạo văn)'], yticklabels=['Thực tế: 0', 'Thực tế: 1'], annot_kws={"size": 14})
    plt.title(f'Ma trận nhầm lẫn (Threshold = {optimal_threshold:.2f})', fontsize=14, pad=15)
    plt.tight_layout()
    cm_path = os.path.join(thu_muc_luu, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()

    # 3. PHÂN TÍCH LỖI FP/FN VÀ XUẤT CSV
    if file_pairs is not None:
        df = pd.DataFrame({'Cặp_File': file_pairs, 'Thực_tế': y_true, 'Dự_đoán': y_pred, 'Điểm_tương_đồng': y_scores})
        
        false_positives = df[(df['Thực_tế'] == 0) & (df['Dự_đoán'] == 1)].copy()
        false_positives['Loại_Lỗi'] = 'False Positive (Bắt oan)'
        
        false_negatives = df[(df['Thực_tế'] == 1) & (df['Dự_đoán'] == 0)].copy()
        false_negatives['Loại_Lỗi'] = 'False Negative (Bỏ lọt)'
        
        error_csv_path = os.path.join(thu_muc_luu, "error_analysis.csv")
        pd.concat([false_positives, false_negatives]).to_csv(error_csv_path, index=False, encoding='utf-8-sig')

    print(f"✅ HOÀN TẤT! Đã lưu toàn bộ file minh chứng vào thư mục: '{thu_muc_luu}'")