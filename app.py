import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Giáo Sư Pi - Gia sư Toán AI", page_icon="🎓", layout="centered")

# Nhúng CSS để giao diện thân thiện với trẻ em
st.markdown("""
    <style>
    .stApp { background-color: #f0f8ff; }
    .stChatMessage { border-radius: 15px; }
    h1 { color: #1E90FF; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- CẤU HÌNH AI ---
# Lưu ý: Thay 'YOUR_API_KEY' bằng key của bạn hoặc dùng Streamlit Secrets
API_KEY = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash') # Model mạnh về Vision & Tốc độ
else:
    st.warning("Vui lòng nhập API Key ở thanh bên để bắt đầu!")

# --- PROMPT HỆ THỐNG (BỘ NÃO CỦA GIÁO SƯ PI) ---
SYSTEM_PROMPT = """
Bạn là "Giáo Sư Pi" - gia sư toán tiểu học (Lớp 1-5) tại Việt Nam.
Nhiệm vụ: Hướng dẫn học sinh giải toán theo phương pháp Socratic (không cho đáp án ngay, đặt câu hỏi gợi mở).
Phong cách: Vui vẻ như Doraemon, sâu sắc như giáo sư. Xưng hô: Thầy Pi - Con.

QUY TRÌNH XỬ LÝ ẢNH:
1. Xác nhận đề bài từ ảnh: "Thầy Pi thấy đề bài là... đúng không con?"
2. Chờ phản hồi hoặc hướng dẫn từng bước nhỏ.
3. Nếu chữ xấu, hãy nhắc nhở nhẹ nhàng.
"""

# --- GIAO DIỆN NGƯỜI DÙNG ---
st.title("🎓 Giáo Sư Pi - Gia sư Toán AI")
st.caption("Con chụp ảnh bài tập hoặc nhắn tin để Thầy Pi hướng dẫn nhé!")

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Chào con! Thầy Pi đã sẵn sàng. Hôm nay có bài toán nào làm khó con sao?"}
    ]

# Hiển thị lịch sử chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHỨC NĂNG TẢI ẢNH ---
uploaded_file = st.file_uploader("📸 Chụp hoặc tải ảnh bài toán", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Ảnh bài toán con gửi", use_column_width=True)

# --- XỬ LÝ NHẬP LIỆU ---
if prompt := st.chat_input("Hỏi Thầy Pi..."):
    # Hiển thị tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gọi AI xử lý
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            input_data = [SYSTEM_PROMPT, prompt]
            if uploaded_file:
                input_data.append(img)
            
            # Gửi tới Gemini
            response = model.generate_content(input_data)
            full_response = response.text
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Có lỗi xảy ra rồi: {e}")

# --- FOOTER ---
st.divider()
st.info("Mẹo: Con nên chụp ảnh rõ nét và đủ ánh sáng để Thầy Pi nhìn chuẩn nhất nhé!")
