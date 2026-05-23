import tokenize
from io import BytesIO

def extract_tokens(code_string):
    """Hàm phân rã mã nguồn thành các token cơ bản"""
    tokens = []
    try:
        # Đọc file từ chuỗi string
        for tok in tokenize.tokenize(BytesIO(code_string.encode('utf-8')).readline):
            # Chỉ lấy các token quan trọng hình thành nên logic code
            if tok.type in [tokenize.NAME, tokenize.OP, tokenize.NUMBER, tokenize.STRING]:
                tokens.append(tok.string)
    except Exception:
        pass
    return tokens

def calculate_statistical_features(code_1, code_2):
    """Hàm tính toán chênh lệch số dòng code"""
    lines_1 = len(code_1.split('\n'))
    lines_2 = len(code_2.split('\n'))
    return abs(lines_1 - lines_2)