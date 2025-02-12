import streamlit as st
import pandas as pd
from threading import Thread
from controller.question_controller import QuestionController
from controller.cot_controller import CoTController
from controller.rag_controller import RAGController
from src.model import EmbeddingModel
from datetime import date, datetime

# Khởi tạo controller và mô hình
controller = QuestionController()
cot_controller = CoTController()
rag_controller = RAGController()
embedding_model = EmbeddingModel()

# File path for storing query history
QUERY_HISTORY_FILE = "query_history.txt"

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
        [data-testid="stSidebarContent"] {
            background-image: url("https://i.postimg.cc/nzz6CQ0c/c92d81ec0f80b635611321e1ff5bfcb9.jpg");
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def inject_custom_css():
    st.markdown("""
        <style>
            body {
                font-family: 'Arial', serif;
            }
            .custom-input {
                padding: 15px;
                font-size: 16px;
                border: 1px solid #007bff;
                border-radius: 25px;
                background-color: #CEF8F3;
                font-family: 'Georgia', serif;
                box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
            }
            .send-button {
                background-color: #F25019;
                border: none;
                color: white;
                padding: 12px 18px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 18px;
            }
            .send-button:hover {
                background-color: #0056b3;
            }
            .stSidebar{
                background-color: #f5dac1;
            }
            .stSidebar h2 {
                color: white !important;
            }
            button {
                background-color: #F25019 !important;
                color: white !important;
                font-size: 13px;
            }
            input[type="date"] {
                color: black !important;
                background-color: #2E3B55 !important;
                border: 1px solid #007bff;
                border-radius: 5px;
                padding: 5px 10px;
            }
        </style>
        """, unsafe_allow_html=True)

def add_query_to_history(query):
    try:
        with open(QUERY_HISTORY_FILE, "a", encoding="utf-8") as file:
            file.write(f"{datetime.now()}|{query}\n")
    except Exception as e:
        st.error(f"Lỗi khi lưu truy vấn: {str(e)}")

def load_queries_from_file():
    try:
        with open(QUERY_HISTORY_FILE, "r", encoding="utf-8") as file:
            queries = [line.strip().split("|", 1)[1] for line in file.readlines()]
        queries.reverse()  # Đảo ngược danh sách để truy vấn mới nhất ở trên cùng
        return queries
    except FileNotFoundError:
        return []
    except Exception as e:
        st.error(f"Lỗi khi đọc file: {str(e)}")
        return []

def load_categories():
    df = pd.read_csv('controller/categories.csv')
    categories = df['category'].tolist()
    categories.insert(0, "Tất cả")
    return categories

def load_sources():
    df = pd.read_csv('controller/source.csv')
    sources = df['source'].tolist()
    sources.insert(0, "Tất cả")
    return sources

def convert_string_to_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def display_query_ui():
    set_background()
    inject_custom_css()

    if 'conversation_history' not in st.session_state:
        st.session_state['conversation_history'] = []

    # Sidebar
    with st.sidebar:
        st.subheader("Tùy chọn Lọc")
        selected_category = st.selectbox("Lọc theo Danh mục", load_categories(), key="category_select")
        selected_source = st.selectbox("Lọc theo Nguồn", load_sources(), key="source_select")
        st.subheader("Lọc theo Ngày xuất bản")
        start_date = st.date_input("Ngày bắt đầu", date(2020, 1, 1))
        end_date = st.date_input("Ngày kết thúc", date.today())

        if start_date > end_date:
            st.warning("Ngày bắt đầu phải nhỏ hơn ngày kết thúc!")

        st.subheader("Lịch sử Truy vấn")
        st.markdown('<p style="color:#1a7d3b;">Dưới đây là các truy vấn gần đây của bạn. Nhấp để chạy lại chúng.</p>', unsafe_allow_html=True)
        query_history = load_queries_from_file()
        if query_history:
            selected_history = st.selectbox("Truy vấn trước đây:", query_history, key='history_select')

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Chạy lại truy vấn"):
                    st.session_state['user_query'] = selected_history
                    if st.session_state['user_query']:
                        try:
                            input_vector = embedding_model.embed_text(st.session_state['user_query']).flatten().tolist()
                            filter_dict = {}
                            if selected_category != "Tất cả":
                                filter_dict["category"] = {"$eq": selected_category}
                            if selected_source != "Tất cả":
                                filter_dict["source"] = {"$eq": selected_source}

                            top_k_vectors = controller.query_by_vector(input_vector, top_k=15, filter=filter_dict)

                            related_articles = []
                            for match in top_k_vectors:
                                article_date = convert_string_to_date(match["metadata"].get("published_date", "N/A"))
                                if article_date and start_date <= article_date <= end_date:
                                    article = {
                                        "title": match["metadata"].get("title", "N/A"),
                                        "url": match["metadata"].get("url", "N/A"),
                                        "content": match["metadata"].get("content", "N/A"),
                                        "published_date": match["metadata"].get("published_date", "N/A")
                                    }
                                    related_articles.append(article)

                            if related_articles:
                                reranked_articles = rag_controller.rerank_articles(st.session_state['user_query'], related_articles, top_k=5)
                                final_answer, cite_list = cot_controller.generate_chain_of_thoughts(reranked_articles, st.session_state['user_query'])

                                st.session_state['conversation_history'].append({
                                    "user": st.session_state['user_query'],
                                    "bot": final_answer,
                                    "cite_list": cite_list
                                })

                        except Exception as e:
                            st.error(f"Lỗi: {str(e)}")

            with col2:
                if st.button("Bắt đầu Phiên mới"):
                    st.session_state['conversation_history'] = []
                    st.session_state['user_query'] = ""
                    st.success("Đã bắt đầu một phiên truy vấn mới.")

    for idx, turn in enumerate(st.session_state['conversation_history']):
        st.markdown(
            f"""
            <div style='text-align: right; margin-bottom: 10px;'>
                <div style='background-color: #E8F4FD; border-radius: 10px; display: inline-block; padding: 10px;'>
                    <strong>Bạn:</strong> {turn['user']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style='text-align: left; margin-bottom: 10px;'>
                <div style='background-color: #F6F6F6; border-radius: 10px; display: inline-block; padding: 10px;'>
                    <strong>DataChatbot:</strong> {turn['bot']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if 'cite_list' in turn:
            st.markdown('<h4 style="color: #0f163d;">📖 Nguồn tham khảo:</h4>', unsafe_allow_html=True)
            for idx, cite in enumerate(turn['cite_list'], start=1):
                cite_title = cite.get("title", "Không có tiêu đề")
                cite_url = cite.get("url", "#")
                cite_date = cite.get("published_date", "Không rõ ngày xuất bản")
                st.markdown(f"[{idx}] **{cite_title}**. Xuất bản vào {cite_date}. Xem tại: [{cite_url}]({cite_url})")

    col1, col2, col3 = st.columns([5, 0.5, 0.5])
    with col1:
        user_query = st.text_input("", value="", key="user_query_input", placeholder="Nhập câu hỏi của bạn...", label_visibility='collapsed')
    with col2:
        send_button = st.button("⬆️", key='submit_button', help='Gửi Truy vấn')
    with col3:
        reset_button = st.button("🆕", key='reset_button', help='Bắt đầu truy vấn mới')

    if reset_button:
        st.session_state['conversation_history'] = []
        st.session_state['user_query'] = ""
        st.success("Đã bắt đầu truy vấn mới.")

    if send_button and user_query:
        st.session_state['user_query'] = user_query
        add_query_to_history(user_query)
        try:
            # Chuyển đổi truy vấn thành vector
            input_vector = embedding_model.embed_text(user_query).flatten().tolist()

            # Xây dựng từ điển lọc
            filter_dict = {}
            if selected_category != "Tất cả":
                filter_dict["category"] = {"$eq": selected_category}
            if selected_source != "Tất cả":
                filter_dict["source"] = {"$eq": selected_source}

            # Truy vấn Pinecone để lấy các kết quả phù hợp nhất
            top_k_vectors = controller.query_by_vector(input_vector, top_k=15, filter=filter_dict)

            # Thu thập các bài viết liên quan và lọc theo khoảng ngày xuất bản
            related_articles = []
            for match in top_k_vectors:
                article_date = convert_string_to_date(match["metadata"].get("published_date", "N/A"))

                # Chỉ bao gồm các bài viết trong khoảng ngày đã chọn
                if article_date and start_date <= article_date <= end_date:
                    article = {
                        "title": match["metadata"].get("title", "N/A"),
                        "url": match["metadata"].get("url", "N/A"),
                        "content": match["metadata"].get("content", "N/A"),
                        "published_date": match["metadata"].get("published_date", "N/A")
                    }
                    related_articles.append(article)

            # **Rerank the articles using RAGController**
            if related_articles:
                reranked_articles = rag_controller.rerank_articles(user_query, related_articles, top_k=5)

                # Sinh Chuỗi Suy Nghĩ (CoT)
                final_answer, cite_list = cot_controller.generate_chain_of_thoughts(reranked_articles, user_query)

                # Lưu câu trả lời và nguồn tham khảo vào session_state
                st.session_state['conversation_history'].append({
                    "user": user_query,
                    "bot": final_answer,
                    "cite_list": cite_list
                })

        except Exception as e:
            st.error(f"Lỗi: {str(e)}")

    elif send_button and not user_query:
        st.warning("Vui lòng nhập câu hỏi.")





