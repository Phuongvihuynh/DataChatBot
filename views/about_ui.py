import streamlit as st
import base64
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
        [data-testid="stSidebar"] {
            background-image: url("https://i.postimg.cc/63XJL1X2/aeaa6356dc8d0ea3560c6868013e83c9.jpg");
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Gọi hàm để áp dụng background
set_background()
def display_about_ui():
    set_background()
    # about_ui()
    # .sidebar - toc a: hover {
    # text - decoration: underline;
    # color:  # 0056b3;
    # }
    st.markdown("""
        <style>
            /* Toàn bộ trang */
            body {
                font-family: Arial, sans-serif;
            }

            /* Sidebar mục lục */
            .stSidebar{
                background-color: #f5dac1;
            }
            .sidebar-toc {
                font-size: 16px;
                margin-bottom: 20px;
                padding: 15px;
                background-color: #f8f9fa; /* Màu nền sáng */
                border: 1px solid #dee2e6; /* Viền mỏng */
                border-radius: 8px; /* Bo góc */
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Hiệu ứng đổ bóng */
            }
            .sidebar-toc ul {
                list-style: none; /* Bỏ gạch đầu dòng */
                padding-left: 0;
            }
            .sidebar-toc li {
                margin-bottom: 10px; /* Khoảng cách giữa các mục */
            }
            .sidebar-toc a {
                color: #007bff; /* Màu xanh nổi bật */
                text-decoration: none;
                font-weight: bold;
            }


            /* Bảng đội ngũ dự án */
            .team-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            .team-table th, .team-table td {
                padding: 12px;
                text-align: left;
                border: 1px solid transparent; /* Ẩn viền */
            }
            .team-table th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            .team-table td {
                background-color: #ffffff;
            }

            /* HTML cuộn mượt */
            html {
                scroll-behavior: smooth;
            }
        </style>
        """, unsafe_allow_html=True)
    # Sidebar mục lục
    st.sidebar.markdown("""
        <div class="sidebar-toc">
            <h4>Mục lục</h4>
            <ul>
                <li><a href="#gioi-thieu">Giới thiệu</a></li>
                <li><a href="#quy-trinh-he-thong">Quy trình hệ thống</a></li>
                <li><a href="#tinh-nang-chinh">Tính năng chính</a></li>
                <li><a href="#doi-ngu-du-an">Đội ngũ dự án</a></li>
                <li><a href="#thong-tin-lien-he">Thông tin liên hệ</a></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Nội dung chính với các phần liên kết neo
    st.title("Giới thiệu về DataChatBot")
    st.title("👱🏻‍♀️👩🏻‍🦰👩🏻👧🏽👧🏾")
    st.markdown('<h2 id="gioi-thieu" style="color: #002D62;">📘 Giới thiệu</h2>', unsafe_allow_html=True)
    st.write("""
    DataBot là một hệ thống truy xuất thông tin thông minh, tích hợp công nghệ LLM hiện đại, được thiết kế nhằm cung cấp câu trả lời chính xác cho các câu hỏi liên quan đến thông tin kinh tế. 
    Với mục tiêu hỗ trợ các nhà phân tích dữ liệu, doanh nghiệp và nhà nghiên cứu, DataBot không chỉ cung cấp thông tin nhanh chóng và hiệu quả mà còn đảm bảo tính minh bạch và độ tin cậy bằng cách đính kèm các tài liệu tham khảo cụ thể. 
    Hệ thống hướng tới việc tối ưu hóa quá trình tìm kiếm và khai thác dữ liệu kinh tế, giúp người dùng đưa ra các quyết định chính xác và kịp thời.
    Một phần quan trọng của DataBot là **DataChatBot**, một nền tảng sử dụng trí tuệ nhân tạo tiên tiến, được thiết kế để truy vấn và truy xuất tin tức kinh tế Việt Nam một cách hiệu quả. 
    DataChatBot kết hợp các mô hình AI hiện đại với kỹ thuật Truy Xuất Thông Tin **Dựa Trên RAG (Retrieval-Augmented Generation)** và **Chuỗi Suy Nghĩ (Chain of Thought - CoT)**. 
    Nhờ vào khả năng phân tích và tổng hợp nội dung tin tức theo ngữ cảnh, hệ thống mang đến cho người dùng các câu trả lời chính xác, phù hợp và có giá trị thực tiễn cao.
        """)

    st.markdown('<h2 id="quy-trinh-he-thong" style="color: #002D62;">🔄 Quy trình hệ thống</h2>', unsafe_allow_html=True)
    st.image("docs/EconVNNewsBot.png", caption="Quy trình hoạt động của hệ thống DataChatBot")
    st.write("""
        Quy trình hoạt động của **DataChatBot** đảm bảo rằng người dùng nhận được câu trả lời chính xác và có tính lý luận. Dưới đây là cái nhìn tổng quan về quy trình:

        1. **Thu thập dữ liệu**: 
           - Các bài báo tin tức được thu thập từ nhiều nguồn tin kinh tế Việt Nam khác nhau qua mô-đun **EconVNNewsCrawl**.
           - Những bài báo này được lưu trữ trong một cơ sở dữ liệu tập trung để phục vụ cho việc phân tích.

        2. **Phân đoạn ngữ nghĩa**:
           - Các bài báo dài được chia thành các đoạn ngữ nghĩa nhỏ hơn, giúp truy xuất chính xác và đảm bảo rằng mỗi đoạn đều liên quan đến truy vấn của người dùng.

        3. **Nhúng văn bản**:
           - Các đoạn văn bản được chuyển đổi thành các biểu diễn vector thông qua **Mô hình nhúng văn bản (jina-embeddings-v3)** và lưu trữ trong **Cơ sở dữ liệu vector** để tìm kiếm nhanh chóng.

        4. **Xử lý truy vấn**:
           - Các truy vấn của người dùng cũng được chuyển đổi thành vector sử dụng **Mô hình nhúng câu hỏi**, để dễ dàng so sánh với dữ liệu đã lưu.

        5. **Tìm kiếm và truy xuất vector**:
           - Hệ thống tìm kiếm trong **Cơ sở dữ liệu vector** để xác định và xếp hạng những nội dung có độ tương đồng cao nhất với truy vấn.

        6. **Chuỗi Suy Nghĩ (CoT)**:
           - Các kết quả hàng đầu được phân tích và tổng hợp qua mô-đun **Chuỗi Suy Nghĩ (CoT)**, kết hợp thông tin từ nhiều nguồn để tạo ra câu trả lời mạch lạc và đầy đủ.

        7. **Sinh câu trả lời**:
           - Câu trả lời cuối cùng được tạo ra, dựa trên thông tin từ nhiều bài viết, cùng với các nguồn tham khảo để tăng tính minh bạch và độ tin cậy.
        """)

    st.markdown('<h2 id="tinh-nang-chinh" style="color: #002D62;">✨ Tính năng chính</h2>', unsafe_allow_html=True)
    st.write("""
        - **EconVNNewsCrawl**: Crawler web tùy chỉnh để thu thập tin tức kinh tế Việt Nam từ các nguồn đáng tin cậy.
        - **Phân đoạn ngữ nghĩa**: Chia nhỏ các bài báo dài thành các đoạn có ý nghĩa để cải thiện hiệu quả truy xuất.
        - **Cơ sở dữ liệu vector**: Sử dụng Pinecone cho tìm kiếm và truy xuất vector một cách hiệu quả.
        - **Chuỗi Suy Nghĩ (CoT)**: Tổng hợp thông tin từ nhiều bài báo để đưa ra các câu trả lời chi tiết và có căn cứ.
        """)

    st.markdown('<h2 id="doi-ngu-du-an" style="color: #002D62;">👩‍💻 Đội ngũ dự án</h2>', unsafe_allow_html=True)
    st.markdown("""
        <table class="team-table">
            <thead>
                <tr>
                    <th>Tên</th>
                    <th>MSSV</th>
                    <th>Lớp</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Huỳnh Phương Vi</td>
                    <td>2156210151</td>
                    <td>QLTT21B</td>
                </tr>
                <tr>
                    <td>Hoàng Ngọc Thúy Quỳnh</td>
                    <td>2156210063</td>
                    <td>QLTT21B</td>
                </tr>
                <tr>
                    <td>Vũ Thị Kiều Trang</td>
                    <td>2156210149</td>
                    <td>QLTT21B</td>
                </tr>
                <tr>
                    <td>Đặng Châu Anh</td>
                    <td>2156210003</td>
                    <td>QLTT21B</td>
                </tr>
                <tr>
                    <td>Mai Thị Diễm Huỳnh</td>
                    <td>2156210028</td>
                    <td>QLTT21B</td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

    st.markdown('<h2 id="thong-tin-lien-he" style="color: #002D62;">📞 Thông tin liên hệ</h2>', unsafe_allow_html=True)
    st.write("""
        <p class="contact-info">
        Mọi thắc mắc hoặc đóng góp ý kiến, vui lòng liên hệ chúng tôi qua:
        <br>- <b>Email:</b> <a href="mailto:hpv1812@gmail.com">hpv1812@gmail.com</a>
        <br>- <b>Điện thoại:</b> +84 385 952 124
        </p>
        """, unsafe_allow_html=True)

if __name__ == '__main__':
    set_background()
    display_about_ui()