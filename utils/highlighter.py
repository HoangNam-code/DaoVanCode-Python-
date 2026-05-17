import html

def highlight_code(original_text, matched_snippets):
    """
    Hàm nhận vào text gốc và danh sách các đoạn code trùng lặp.
    Trả về chuỗi HTML đã được bôi màu để hiển thị trên Streamlit.
    """
    # Escape HTML để code không bị lỗi hiển thị khi render trên web
    escaped_text = html.escape(original_text)
    
    # Thay thế dấu xuống dòng bằng thẻ <br> của HTML
    escaped_text = escaped_text.replace('\n', '<br>')
    
    # Quét qua từng đoạn code trùng lặp để bôi màu
    for snippet in matched_snippets:
        # Cần escape snippet y hệt như text gốc để replace chính xác
        escaped_snippet = html.escape(snippet).replace('\n', '<br>')
        
        # Bôi nền vàng, chữ đỏ cho đoạn vi phạm
        highlighted = f'<span style="background-color: #ffe066; color: red; font-weight: bold; border-radius: 3px; padding: 2px;">{escaped_snippet}</span>'
        
        # Thay thế đoạn text bình thường bằng đoạn đã bôi màu
        escaped_text = escaped_text.replace(escaped_snippet, highlighted)
        
    return escaped_text