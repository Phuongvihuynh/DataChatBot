import streamlit as st
from views.streamlit_ui import display_query_ui  # Cho trang tìm kiếm
from views.about_ui import display_about_ui  # Cho trang giới thiệu
from views.user_login import login, register, reset_password, forgot_password
# from views.user_login import login, register
from views.user_login import welcome_screen # Giao diện chào mừng từ user_signup.py
from views.feedback import feedback_form


# Menu Sidebar cho điều hướng
def sidebar_menu():
    st.sidebar.title("📄 DataChatBot")
    st.sidebar.subheader("🔍 Điều hướng")
    return st.sidebar.selectbox("Chọn trang", ["Tìm kiếm", "Giới thiệu", "Báo lỗi/Đóng góp", "Đăng xuất"])

# Trang thông điệp chào mừng
def display_welcome_message():
    st.markdown(
        '<h3 class="header">DataChatBot: Hệ thống suy luận dựa trên truy xuất thông tin cho trả lời câu hỏi về tin tức kinh tế Việt Nam</h3>',
        unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size: 18px;">Hệ thống này cung cấp các câu trả lời chính xác, dựa trên bối cảnh từ một kho tin tức kinh tế Việt Nam rộng lớn, được hỗ trợ bởi suy luận RAT và các nguồn tham khảo uy tín.</p>',
        unsafe_allow_html=True)


def logout_handler():
    st.markdown("""
            <style>
            [data-testid="stAppViewContainer"] {
            background-image: url("https://i.postimg.cc/nzz6CQ0c/c92d81ec0f80b635611321e1ff5bfcb9.jpg");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        [data-testid="stHeader"] {
            background: rgba(0, 0, 0, 0);
        }
                /* Toàn bộ trang */
                body {
                    font-family: Arial, sans-serif;
                }
                .stSidebar{
                background-color: #f5dac1;
            }
            </style>
            """, unsafe_allow_html=True)
    # Hiển thị một thông báo xác nhận
    st.markdown("## Bạn có chắc chắn muốn đăng xuất khỏi ứng dụng?")
    col1, col2 = st.columns(2)

    # Hai nút xác nhận: "Có" và "Không"
    with col1:
        if st.button("Có"):
            # Xử lý đăng xuất
            st.session_state["is_logged_in"] = False
            st.session_state.logged_in = False
            st.session_state.show_main_ui = False
            st.success("Bạn đã đăng xuất thành công!")

    with col2:
        if st.button("Không"):
            # Quay lại giao diện chính
            st.info("Bạn đã hủy thao tác đăng xuất.")


# Hàm chính của ứng dụng
def main():

    # Nếu chưa đăng nhập, hiển thị giao diện đăng nhập/đăng ký
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        with st.expander('DataChatBot', expanded=True):
            login_tab, create_tab, forgot_password_tab, reset_password_tab = st.tabs([
                "Đăng nhập", "Tạo tài khoản", "Quên mật khẩu", "Đặt lại mật khẩu"
            ])

            with login_tab:
                login()
            with create_tab:
                register()  # Hàm đăng ký từ trước
            with forgot_password_tab:
                forgot_password()  # Hàm quên mật khẩu
            with reset_password_tab:
                reset_password()  # Hàm đặt lại mật khẩu

    # Nếu đã đăng nhập, hiển thị màn hình chào mừng
    elif not st.session_state.get("show_main_ui", False):
        welcome_screen()

    # Khi người dùng nhấn "Bắt đầu khám phá", hiển thị giao diện chính
    else:
        # Điều hướng Sidebar
        selected_page = sidebar_menu()  # Hàm tạo menu bên trái

        # Điều hướng giữa các trang dựa vào lựa chọn của người dùng
        if selected_page == "Tìm kiếm":
            display_welcome_message()
            display_query_ui()
        elif selected_page == "Giới thiệu":
            display_about_ui()
        elif selected_page == "Báo lỗi/Đóng góp":
            feedback_form()
        elif selected_page == "Đăng xuất":
            logout_handler()  # Hàm xử lý đăng xuất
        # Điểm bắt đầu chính của ứng dụng
if __name__ == "__main__":
    main()




