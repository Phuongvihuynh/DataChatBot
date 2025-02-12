from datetime import datetime
from crawlers.cafebiz_crawler import CafebizCrawler
from crawlers.cafef_crawler import CafefCrawler
from crawlers.vnexpress_crawler import VNExpressCrawler
from crawlers.vietnamnet_crawler import VietnamnetCrawler  # Thêm VietnamnetCrawler

def main():
    # Tạo từ điển ánh xạ các lựa chọn từ người dùng với các lớp crawler tương ứng
    crawlers = {
        "1": CafebizCrawler(),
        "2": CafefCrawler(),
        "3": VNExpressCrawler(),
        "4": VietnamnetCrawler(),  # Thêm lựa chọn Vietnamnet
    }

    # Hiển thị tùy chọn cho người dùng
    print("Select the source to scrape:")
    print("1: Cafebiz")
    print("2: Cafef")
    print("3: VNExpress")
    print("4: Vietnamnet")  # Thêm lựa chọn Vietnamnet

    # Nhận đầu vào từ người dùng
    source_choice = input("Enter the number corresponding to the source (1, 2, 3, or 4): ")

    if source_choice not in crawlers:
        print("Invalid selection. Please select a valid option (1, 2, 3, or 4).")
        return

    # Nhận ngày bắt đầu và kết thúc từ người dùng
    try:
        start_date = datetime.strptime(input("Enter start date (YYYY-MM-DD): "), "%Y-%m-%d")
        end_date = datetime.strptime(input("Enter end date (YYYY-MM-DD): "), "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    if start_date > end_date:
        print("Start date cannot be after the end date.")
        return

    # Khởi tạo crawler dựa trên lựa chọn của người dùng
    selected_crawler = crawlers[source_choice]

    # Thu thập dữ liệu
    articles = selected_crawler.collect_articles_between_dates(start_date, end_date)

    if not articles:
        print(f"No articles found for the selected dates from {selected_crawler.__class__.__name__}.")
        return

    # Lưu dữ liệu vào file JSON
    output_file = f"data/{selected_crawler.__class__.__name__.lower()}_articles_{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        import json
        json.dump(articles, f, ensure_ascii=False, indent=4)

    print(f"Collected {len(articles)} articles from {selected_crawler.__class__.__name__}. Saved to {output_file}.")

if __name__ == "__main__":
    main()
