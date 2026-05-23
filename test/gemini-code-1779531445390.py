# Hàm tính điểm trung bình và xếp loại sinh viên
def tinh_diem_trung_binh(toan, ly, hoa):
    dtb = (toan + ly + hoa) / 3
    return dtb

def xep_loai(dtb):
    if dtb >= 8.0:
        return "Giỏi"
    elif dtb >= 6.5:
        return "Khá"
    elif dtb >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

danh_sach = [
    {"ten": "Nam", "toan": 8, "ly": 7, "hoa": 9},
    {"ten": "Hoa", "toan": 5, "ly": 6, "hoa": 5}
]

for sv in danh_sach:
    diem = tinh_diem_trung_binh(sv["toan"], sv["ly"], sv["hoa"])
    loai = xep_loai(diem)
    print(f'Sinh viên {sv["ten"]} - Điểm: {diem:.2f} - Loại: {loai}')