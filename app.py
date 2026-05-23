import streamlit as st
import matplotlib.pyplot as plt
import sys
import os
from utils.highlighter import highlight_code

# Thêm thư mục gốc vào đường dẫn hệ thống để fix lỗi ModuleNotFoundError
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.preprocess_code import lam_sach_code
from src.jaccard_baseline import jaccard_similarity

# -- CẤU HÌNH TRANG WEB --
st.set_page_config(page_title="Hệ Thống Phát Hiện Đạo Văn", layout="wide")
st.title("🔍 Hệ Thống Phát Hiện Đạo Văn Code Python")

# -- GIAO DIỆN UPLOAD FILE (SIDE-BY-SIDE) --
st.markdown("### 1. Tải lên bài tập cần kiểm tra")
col1, col2 = st.columns(2)

with col1:
    file1 = st.file_uploader("Tải lên Bài tập 1", type=["py", "txt", "c", "cpp", "java", "html", "docx"])
with col2:
    file2 = st.file_uploader("Tải lên Bài tập 2", type=["py", "txt", "c", "cpp", "java", "html", "docx"])

# -- NÚT CHẠY KIỂM TRA --
if st.button("🚀 Xử lý & Kiểm tra đạo văn"):
    if file1 is not None and file2 is not None:
        # Đọc nội dung file gốc
        text1 = file1.read().decode("utf-8")
        text2 = file2.read().decode("utf-8")
        
        with st.spinner('Đang phân tích dữ liệu...'):
            # ==========================================
            # KHU VỰC TÍCH HỢP CODE THÀNH VIÊN 1 & 2
            # ==========================================
            
            # 1. Gọi logic làm sạch code (Xóa comment, chuẩn hóa khoảng trắng)
            cleaned1 = lam_sach_code(text1)
            cleaned2 = lam_sach_code(text2)
            
            # 2. Tính phần trăm đạo văn thực tế bằng thuật toán Jaccard
            similarity_score = jaccard_similarity(cleaned1, cleaned2)
            percent = round(similarity_score * 100, 2)
            
            # 3. Trích xuất các đoạn code giống nhau để bôi màu đối soát
            # Tách nội dung thành từng dòng
            original_lines1 = text1.split('\n')
            original_lines2 = text2.split('\n')
            
            # Dùng dictionary để map từ dòng đã xóa khoảng trắng thừa -> dòng gốc nguyên bản
            dict_lines1 = {line.strip(): line for line in original_lines1 if len(line.strip()) > 10}
            dict_lines2 = {line.strip(): line for line in original_lines2 if len(line.strip()) > 10}
            
            # Lấy các dòng code trùng lặp (Intersection)
            common_stripped_lines = set(dict_lines1.keys()).intersection(set(dict_lines2.keys()))
            
            # Lấy lại định dạng dòng gốc để highlighter có thể nhận diện và bôi màu chính xác
            matched_snippets = [dict_lines1[line] for line in common_stripped_lines]
            # ==========================================
            
        # -- HIỂN THỊ KẾT QUẢ TỶ LỆ (%) --
        st.markdown("---")
        st.markdown("### 2. Kết quả tổng quan")
        
        # Vẽ biểu đồ hình tròn (Pie chart)
        fig, ax = plt.subplots(figsize=(3, 3))
        ax.pie([percent, 100-percent], labels=[f"Đạo văn ({percent}%)", "Khác biệt"], 
               colors=["#ff9999", "#66b3ff"], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  
        
        # Hiển thị biểu đồ và thanh Progress bar
        col_chart, col_progress = st.columns([1, 2])
        with col_chart:
            st.pyplot(fig)
        with col_progress:
            st.write(f"**Mức độ trùng lặp:** {percent}%")
            st.progress(int(percent))
            if percent > 50:
                st.error("Cảnh báo: Mức độ trùng lặp cao!")
            else:
                st.success("Mức độ trùng lặp ở ngưỡng an toàn.")

        # -- HIỂN THỊ CHI TIẾT ĐỐI SOÁT (SIDE-BY-SIDE) --
        st.markdown("---")
        st.markdown("### 3. Đối soát chi tiết (Phần bôi màu)")
        
        # Gọi logic bôi màu từ highlighter.py
        highlighted_text1 = highlight_code(text1, matched_snippets)
        highlighted_text2 = highlight_code(text2, matched_snippets)
        
        # Hiển thị 2 cột song song
        c1, c2 = st.columns(2)
        
        # Dùng HTML/CSS để tạo khung chứa code có thanh cuộn
        box_style = """
        <div style='height: 400px; overflow-y: scroll; border: 1px solid #ccc; 
                    padding: 10px; border-radius: 5px; background-color: #f8f9fa; font-family: monospace;'>
            {}
        </div>
        """
        
        with c1:
            st.markdown(f"**Nội dung Bài tập 1:**")
            st.markdown(box_style.format(highlighted_text1), unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"**Nội dung Bài tập 2:**")
            st.markdown(box_style.format(highlighted_text2), unsafe_allow_html=True)

    else:
        st.warning("Vui lòng tải lên đầy đủ 2 file bài tập trước khi kiểm tra!")