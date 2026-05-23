"""
Chương trình đánh giá học lực học sinh
(Bản sao chép đã bị thay đổi tên hàm, tên biến và cấu trúc khoảng trắng)
"""

def calc_avg(m1, m2, m3):
    # Tính trung bình cộng 3 môn
    avg_score = (m1 + m2 + m3) / 3.0
    return avg_score

def get_rank(score):
    if score >= 8.0: return "Giỏi"
    if score >= 6.5: return "Khá"
    if score >= 5.0: return "Trung bình"
    return "Yếu"

students = [
    {"ten": "Nam", "toan": 8, "ly": 7, "hoa": 9},
    {"ten": "Hoa", "toan": 5, "ly": 6, "hoa": 5}
]

for s in students:
    # Gọi hàm tính toán
    avg = calc_avg(s["toan"], s["ly"], s["hoa"])
    rank = get_rank(avg)
    print(f'Sinh viên {s["ten"]} - Điểm: {avg:.2f} - Loại: {rank}')