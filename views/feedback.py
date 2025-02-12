import streamlit as st
from datetime import datetime

FILE_PATH = "feedback_customer.txt"

def save_feedback_to_file(feedback, email):
    try:
        feedback = feedback.replace("\n", " \\n ")
        with open(FILE_PATH, "a", encoding="utf-8") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp}|{email}|{feedback}\n")
    except Exception as e:
        st.error(f"Lỗi khi lưu vào file: {str(e)}")

def get_all_feedback_from_file():
    feedback_list = []
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            for line in file:
                timestamp, email, feedback = line.strip().split("|", 2)
                # Khôi phục dòng mới từ "\\n" thành "\n" khi đọc
                feedback = feedback.replace(" \\n ", "\n")
                feedback_list.append((timestamp, email, feedback))
    except FileNotFoundError:
        st.warning("Chưa có phản hồi nào được lưu!")
    except Exception as e:
        st.error(f"Lỗi khi đọc file: {str(e)}")
    return feedback_list

def set_background():
    st.markdown(
        """
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
        textarea, input[type="text"] {
            background-color: white !important;
            color: black !important;
            border: 1px solid #ccc !important;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            padding: 10px;
        }
        .stButton>button {
            background-color: #F25019 !important;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def feedback_form():
    st.markdown(
        """
        <style>
        body {
            font-family: Arial, sans-serif;
        }
        .stSidebar{
            background-color: #f5dac1;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    set_background()
    st.title("📩 Báo lỗi hoặc Góp ý")
    st.markdown(
        """
        Sự đóng góp ý kiến từ các bạn sẽ là sự hỗ trợ đắc lực giúp chúng tôi ngày càng tốt hơn. 
        Vui lòng điền vào mẫu dưới đây.
        """,
        unsafe_allow_html=True,
    )

    # Feedback form
    with st.form(key="feedback_form", clear_on_submit=True):
        user_feedback = st.text_area("Nhập phản hồi của bạn tại đây!", placeholder="Nhập ý kiến phản hồi...")
        user_email = st.text_input("Email của bạn", placeholder="name@example.com")
        submit_button = st.form_submit_button(label="Gửi ý kiến")

        if submit_button:
            if user_feedback and user_email:
                save_feedback_to_file(user_feedback, user_email)
                st.success("🎉 Cảm ơn bạn đã gửi ý kiến!")
            else:
                st.warning("Vui lòng điền đầy đủ thông tin!")

    # st.subheader("📋 Các phản hồi đã gửi")
    # feedback_list = get_all_feedback_from_file()
    # for feedback in feedback_list:
    #     st.markdown(f"""
    #     **Email:** {feedback[1]}
    #     **Phản hồi:**
    #     {feedback[2]}
    #     **Thời gian:** {feedback[0]}
    #     ---
    #     """)


if __name__ == "__main__":
    feedback_form()


# import sqlite3
# import streamlit as st
# from datetime import datetime
#
# # Hàm khởi tạo cơ sở dữ liệu
# def init_db():
#     conn = sqlite3.connect("../feedback_customer.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS feedback (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             feedback TEXT NOT NULL,
#             email TEXT NOT NULL,
#             timestamp TEXT NOT NULL
#         )
#     """)
#     conn.commit()
#     conn.close()
#
# # Hàm lưu phản hồi vào cơ sở dữ liệu
# def save_feedback(feedback, email):
#     conn = sqlite3.connect("../feedback_customer.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO feedback (feedback, email, timestamp)
#         VALUES (?, ?, ?)
#     """, (feedback, email, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#     conn.commit()
#     conn.close()
#
# # Hàm lấy tất cả phản hồi
# def get_all_feedback():
#     conn = sqlite3.connect("../feedback.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM feedback ORDER BY timestamp DESC")
#     rows = cursor.fetchall()
#     conn.close()
#     return rows
#
# # Hàm đặt background
# def set_background():
#     st.markdown(
#         """
#         <style>
#         [data-testid="stAppViewContainer"] {
#             background-image: url("https://i.postimg.cc/nzz6CQ0c/c92d81ec0f80b635611321e1ff5bfcb9.jpg");
#             background-size: cover;
#             background-position: center center;
#             background-repeat: no-repeat;
#             background-attachment: fixed;
#         }
#         [data-testid="stHeader"] {
#             background: rgba(0, 0, 0, 0);
#         }
#         textarea, input[type="text"] {
#             background-color: white !important; /* Đặt màu nền trắng */
#             color: black !important; /* Màu chữ đen */
#             border: 1px solid #ccc !important; /* Viền nhẹ */
#             border-radius: 5px; /* Bo góc */
#             box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); /* Bóng mờ */
#             padding: 10px; /* Thêm khoảng cách bên trong */
#         }
#         .stButton>button {
#             background-color: #F25019 !important;;
#             color: white;
#             }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )
#
# # Giao diện chính
# def feedback_form():
#     st.markdown("""
#         <style>
#             /* Toàn bộ trang */
#             body {
#                 font-family: Arial, sans-serif;
#             }
#             .stSidebar{
#             background-color: #f5dac1;
#
#         }
#         </style>
#         """, unsafe_allow_html=True)
#     set_background()
#     st.title("📩 Báo lỗi hoặc Góp ý")
#     st.markdown(
#         """
#         Sự đóng góp ý kiến từ các bạn sẽ là sự hỗ trợ đắc lực giúp chúng tôi ngày càng tốt hơn.
#         Vui lòng điền vào mẫu dưới đây.
#         """,
#         unsafe_allow_html=True,
#     )
#
#     # Form nhập ý kiến
#     with st.form(key="feedback_form", clear_on_submit=True):
#         user_feedback = st.text_area("Nhập phản hồi của bạn tại đây!", placeholder="Nhập ý kiến phản hồi...")
#         user_email = st.text_input("Email của bạn", placeholder="name@example.com")
#         submit_button = st.form_submit_button(label="Gửi ý kiến")
#
#         if submit_button:
#             if user_feedback and user_email:
#                 save_feedback(user_feedback, user_email)
#                 st.success("🎉 Cảm ơn bạn đã gửi ý kiến!")
#             else:
#                 st.warning("Vui lòng điền đầy đủ thông tin!")
#
#     # Hiển thị tất cả phản hồi
#     # st.subheader("📋 Các phản hồi đã gửi")
#     # feedback_list = get_all_feedback()
#     # for feedback in feedback_list:
#     #     st.markdown(f"""
#     #     **Email:** {feedback[2]}
#     #     **Phản hồi:** {feedback[1]}
#     #     **Thời gian:** {feedback[3]}
#     #     ---
#     #     """)
#
# # Khởi chạy ứng dụng
# if __name__ == "__main__":
#     init_db()  # Khởi tạo cơ sở dữ liệu
#     feedback_form()


