import streamlit as st
import yaml
import hashlib
import os
from views.global_settings import USERS_FILE
import base64
import string
import random

def signin_ui():
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    .stExpander {{
        background-color: rgba(255, 255, 255, 0.95) !important; /* Nền trắng tinh tế */
        border: 1px solid #EDEDED !important; /* Viền sáng nhẹ */
        border-radius: 15px !important; /* Bo góc */
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important; /* Đổ bóng nhẹ */
        padding: 20px !important; /* Cân chỉnh khoảng cách bên trong */
    }}
    .stTabs [role="tablist"] {{
        margin-bottom: 15px !important; /* Tăng khoảng cách giữa tabs và nội dung */
    }}
    .stTextInput input {{
        background-color: #F9F9F9 !important; /* Nền sáng mờ */
        border: 1px solid #DDD !important; /* Viền nhẹ */
        padding: 12px !important; /* Khoảng cách lớn hơn */
        border-radius: 10px !important; /* Bo tròn góc ô nhập liệu */
        font-size: 15px !important; /* Tăng kích cỡ chữ */
        font-family: 'Arial', sans-serif !important; /* Phông chữ hiện đại */
    }}
    .stButton>button {{
        background: linear-gradient(135deg, #FF7F50, #FF4500) !important; /* Gradient nút */
        color: white !important; /* Chữ màu trắng */
        font-size: 16px !important; /* Tăng kích thước chữ */
        font-weight: bold !important; /* Chữ đậm */
        padding: 10px 20px !important; /* Tăng kích thước nút */
        border: none !important; /* Loại bỏ viền */
        border-radius: 8px !important; /* Bo góc nút */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important; /* Hiệu ứng nổi */
        cursor: pointer !important; /* Thay đổi con trỏ */
        transition: all 0.3s ease !important; /* Hiệu ứng hover mượt */
    }}
    .stButton>button:hover {{
        transform: translateY(-3px) !important; /* Di chuyển nút lên trên khi hover */
        background: linear-gradient(135deg, #FF6347, #FF0000) !important; /* Gradient đậm hơn */
    }}
    .stTextInput label {{
        font-weight: 600 !important; /* Tăng độ đậm nhãn */
        font-size: 14px !important; /* Kích thước chữ */
        color: #333 !important; /* Màu tối hơn */
        font-family: 'Roboto', sans-serif !important; /* Phông chữ nhãn */
        margin-bottom: 5px; /* Khoảng cách nhãn với ô nhập */
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)


def load_users():
    if os.path.exists(USERS_FILE) and os.path.getsize(USERS_FILE) > 0:
        with open(USERS_FILE, 'r') as file:
            users = yaml.safe_load(file)
        return users
    else:
        return {"usernames": {}}



def save_users(users):
    with open(USERS_FILE, 'w') as file:
        yaml.safe_dump(users, file)



def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(stored_password, provided_password):
    return stored_password == hash_password(provided_password)


def register():
    with st.form(key="register"):
        st.subheader('Đăng ký')
        username = st.text_input('Tên tài khoản')
        email = st.text_input('Email')
        name = st.text_input('Họ tên')
        password = st.text_input('Mật khẩu', type='password')
        confirm_password = st.text_input('Xác nhận mật khẩu', type='password')

        if st.form_submit_button('Đăng ký'):
            users = load_users()
            if len(users['usernames']) >= 10:
                st.error('Số lượng người dùng đã đạt giới hạn tối đa!')
            elif not username or not password:
                st.error('Bạn cần nhập tên tài khoản và mật khẩu!')
            elif password == confirm_password:
                if username in users['usernames']:
                    st.error('Tên tài khoản không hợp lệ!')
                else:
                    hashed_password = hash_password(password)
                    users['usernames'][username] = {
                        'email': email,
                        'name': name,
                        'password': hashed_password
                    }
                    save_users(users)
                    st.session_state.username = username
                    st.session_state.logged_in = True
                    st.session_state.user_info = f"username:{username}, "
                    for key, value in users['usernames'][username].items():
                        if key != 'password':
                            st.session_state.user_info = st.session_state.user_info + f"{key}:{value}, "
                    st.rerun()
            else:
                st.error('Mật khẩu không khớp!')


def login():
    with st.form(key="login"):
        username = st.text_input('👤 Tên đăng nhập')
        password = st.text_input('🔒 Mật khẩu', type='password')

        if st.form_submit_button('Đăng nhập'):
            users = load_users()
            if username in users['usernames']:
                stored_password = users['usernames'][username]['password']
                if verify_password(stored_password, password):
                    st.session_state.username = username
                    st.session_state.logged_in = True
                    st.session_state.user_info = f"username:{username}, "
                    for key, value in users['usernames'][username].items():
                        if key != 'password':
                            st.session_state.user_info = st.session_state.user_info + f"{key}:{value}, "
                    st.rerun()
                else:
                    st.error('Mật khẩu không chính xác!')
            else:
                st.error('Tên đăng nhập không đúng!')


def generate_temp_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


def forgot_password():
    st.subheader("Quên mật khẩu")
    username = st.text_input("Tên tài khoản")
    email = st.text_input("Email đã đăng ký")

    if st.button("Xác nhận"):
        users = load_users()
        if username in users['usernames'] and users['usernames'][username]['email'] == email:
            # Tạo mật khẩu tạm thời
            temp_password = generate_temp_password()
            hashed_password = hash_password(temp_password)
            users['usernames'][username]['password'] = hashed_password
            save_users(users)

            st.success(f"Mật khẩu tạm thời của bạn là: {temp_password}")
            st.info("Vui lòng đăng nhập lại và thay đổi mật khẩu của bạn.")
        else:
            st.error("Tên tài khoản hoặc email không đúng!")


# Reset mật khẩu (Reset Password)
def reset_password():
    st.subheader("Đổi mật khẩu")
    old_password = st.text_input("Mật khẩu hiện tại", type="password")
    new_password = st.text_input("Mật khẩu mới", type="password")
    confirm_new_password = st.text_input("Xác nhận mật khẩu mới", type="password")

    if st.button("Đổi mật khẩu"):
        if st.session_state.username:
            users = load_users()
            username = st.session_state.username
            if verify_password(users['usernames'][username]['password'], old_password):
                if new_password == confirm_new_password:
                    hashed_new_password = hash_password(new_password)
                    users['usernames'][username]['password'] = hashed_new_password
                    save_users(users)
                    st.success("Đổi mật khẩu thành công!")
                else:
                    st.error("Mật khẩu mới không khớp!")
            else:
                st.error("Mật khẩu hiện tại không chính xác!")
        else:
            st.error("Bạn chưa đăng nhập!")

def guest_login():
    if st.button('Khách đăng nhập'):
        st.session_state.logged_in = True
        st.session_state.username = 'Khách'
        st.session_state.user_info = f"username:{st.session_state.username}, " + "Chưa cung cấp thông tin"
        st.rerun()


def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("image\c92d81ec0f80b635611321e1ff5bfcb9.jpg")

import base64


def welcome_screen():
    img = f"""
    <style>
        body {{
            font-family: 'Poppins', serif;
        }}

        [data-testid="stAppViewContainer"] {{
            background-image: url("https://i.postimg.cc/nzz6CQ0c/c92d81ec0f80b635611321e1ff5bfcb9.jpg");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"] {{
            background: rgba(0, 0, 0, 0);
        }}
    .center {{
    text-align: center;
    margin-top: -5px; 
    }}
        .title {{
            font-size: 40px;
            font-weight: bold;
            color: #002D62; 
            margin-top: -10px;
        }}
        .subtitle {{
            font-size: 20px;
            color: black; 
            margin-top: 5px;
        }}
        .button-container {{
            text-align: center;
            margin-top: 10px; 
        }}
        .stButton>button {{
            background-color: #F25019 !important;;
            color: white;
            font-size: 14px;
            padding: 5px 10px;
            margin: 10px 100px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);

        }}
        .stButton>button:hover {{
            background-color: #FF5C00;
        }}
        .image-container {{
            text-align: center;
            margin-top: -5px; 
        }}
        .container {{
            position: relative;
            top: -200px; /* Đưa toàn bộ nội dung lên cao hơn */
        }}
    </style>
    """

    def get_base64_image(file_path):
        with open(file_path, "rb") as file:
            return base64.b64encode(file.read()).decode("utf-8")

    st.markdown(img, unsafe_allow_html=True)
    image_base64 = get_base64_image("image/67eee165970d82eae6faa0266ce4ec06.jpg")
    st.markdown(
        f"""
            <div class="center">
                <p class="title" style="font-size: 40px;">🎆 CHÀO MỪNG <strong>{st.session_state.username}</strong>  đến với Chatbot của chúng tôi!🎇</p>
                <p class="subtitle">We are USSHers | Đây là đồ án tốt nghiệp của tụi mình</p>
            </div>

        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button('Nhấn để bắt đầu'):
            # Chuyển đến giao diện chính
            st.session_state.show_main_ui = True
            st.rerun()
    st.markdown(
        f"""
            <div class="image-container">
                <img src="data:image/png;base64,{image_base64}" alt="Laptop Image" style="border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
            </div>
        """,
        unsafe_allow_html=True,
    )
# def welcome_screen():
#     # Hàm để load và encode ảnh avatar
#     def load_image_as_base64(image_path):
#         with open(image_path, "rb") as img_file:
#             return base64.b64encode(img_file.read()).decode()
#
#     # Load ảnh từ file (thay đường dẫn bằng tệp của bạn)
#     image_path = "image/153492d5cc36e23919920d27ab4b08cc.jpg"  # Thay bằng đường dẫn ảnh của bạn
#     image_base64 = load_image_as_base64(image_path)
#
#     # CSS tùy chỉnh
#     st.markdown(
#         """
#         <style>
#                     body {
#                     font-family: 'Paytone One', serif;
#                 }
#             .center {
#                 text-align: center;
#             }
#             .title {
#                 font-size: 100px;
#                 font-weight: bold;
#                 color: #FF4500;
#             }
#             .subtitle {
#                 font-size: 50px;
#                 color: #333333;
#                 margin-bottom: 20px;
#             }
#             .welcome-box {
#                 background-color: #FFF3E0;
#                 padding: 20px;
#                 width: 100%;
#                 border-radius: 15px;
#                 box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
#                 display: inline-block;
#                 text-align: center;
#             }
#             .avatar {
#                 width: 100px;
#                 height: 100px;
#                 border-radius: 50%;
#                 margin-bottom: 10px;
#                 padding-top: -50px;
#             }
#             .button {
#                 background-color: #FF5722;
#                 color: white;
#                 font-size: 16px;
#                 font-weight: bold;
#                 padding: 10px 20px;
#                 border: none;
#                 border-radius: 5px;
#                 cursor: pointer;
#                 margin-top: 20px;
#                 box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
#             }
#             .button:hover {
#                 background-color: #E64A19;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
#
#     # Hiển thị nội dung giao diện
#     st.markdown('<div class="center"><h1>Welcome to | <span style="color:#FF5722;">USSHer - CHATBOT</span></h1></div>',
#                 unsafe_allow_html=True)
#
#     st.markdown(
#         f"""
#         <div class="center">
#             <div class="welcome-box">
#                 <img class="avatar" src="data:image/png;base64,{image_base64}" alt="Avatar">
#                 <p class="title">Chào mừng, <strong>{st.session_state.username}</strong></p>
#                 <p class="subtitle">Hôm nay chúng tôi có thể giúp gì cho bạn? <br> Hãy cùng khám phá nhé!</p>
#                 <button class="button" onclick="sendData()">Vào thôi!!!</button>
#             </div>
#         </div>
#
#         <script>
#             function sendData() {{
#                 // Gửi một yêu cầu POST giả lập để kích hoạt logic Python
#                 fetch("/?action=start", {{ method: "POST" }})
#                 .then(() => {{
#                     // Làm mới trang sau khi gửi dữ liệu
#                     window.location.reload();
#                 }});
#             }}
#         </script>
#         """,
#         unsafe_allow_html=True,
#     )
#
#     # Đọc action từ query params (nếu có)
#     if "action" in st.query_params and st.query_params["action"] == ["start"]:
#         st.session_state.show_main_ui = True
#         st.rerun()

# Sử dụng hai chức năng này
if __name__ == '__main__':
    signin_ui()
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        with st.expander('USSHerDataQueryChatBot', expanded=True):
            login_tab, create_tab, forgot_tab = st.tabs(
                [
                    "Đăng nhập",
                    "Tạo tài khoản",
                    "Quên mật khẩu",
                ]
            )
            with create_tab:
                register()
            with login_tab:
                login()
            with forgot_tab:
                forgot_password()
    else:
        with st.expander('Tài khoản của bạn', expanded=True):
            welcome_tab, reset_tab = st.tabs(
                [
                    "Chào mừng",
                    "Đổi mật khẩu",
                ]
            )
            with welcome_tab:
                welcome_screen()
            with reset_tab:
                reset_password()