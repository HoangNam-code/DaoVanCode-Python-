import streamlit as st
import matplotlib.pyplot as plt
from utils.highlighter import highlight_code

# Import code của Thành viên 1 và 2 (Bỏ comment khi đã có code thực tế)
# from utils.member1_cleaner import clean_code
# from utils.member2_logic import calculate_plagiarism

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
            
            # 1. Gọi code Thành viên 1 (Làm sạch)
            # cleaned1 = clean_code(text1)
            # cleaned2 = clean_code(text2)
            
            # 2. Gọi code Thành viên 2 (Tính %)
            # percent, matched_snippets = calculate_plagiarism(cleaned1, cleaned2)
            
            # --- DỮ LIỆU GIẢ LẬP ĐỂ TEST GIAO DIỆN CHẠY TRƯỚC ---
            percent = 45.0  # Giả lập tỷ lệ
            matched_snippets = [
                "int calculateSum(int a, int b) {", 
                "return a + b;",
                "}"
            ] # Giả lập 2 dòng code bị Thành viên 2 bắt lỗi giống nhau
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