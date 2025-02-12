from crawlers.base_crawler import BaseCrawler
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class VNExpressCrawler(BaseCrawler):
    def date_to_timestamp(self, date_obj):
        """Chuyển đổi datetime sang Unix timestamp"""
        return int(date_obj.timestamp())

    def extract_article_details(self, article_url):
        """Lấy chi tiết bài báo từ URL bài báo"""
        article_html = self.fetch_html(article_url)
        if article_html is None:
            return None

        soup = BeautifulSoup(article_html, 'html.parser')

        # Lấy tiêu đề
        title = soup.find('h1', class_='title-detail').get_text(strip=True) if soup.find('h1', class_='title-detail') else ""

        # Lấy nội dung
        content_paragraphs = soup.find_all('p')
        content = "\n".join([para.get_text(strip=True) for para in content_paragraphs]) if content_paragraphs else ""

        # Lấy ngày đăng bài
        published_date = soup.find('span', class_='date').get_text(strip=True) if soup.find('span', class_='date') else ""

        # Lấy tên tác giả
        author_info = "Unknown"
        if len(content_paragraphs) > 0:
            last_line = content_paragraphs[-1].get_text(strip=True)
            if last_line:
                author_info = last_line.split(",")[0].strip()

        # Lấy chuyên mục
        breadcrumb = soup.find('ul', class_='breadcrumb')
        category_tag = breadcrumb.find('li').find('a') if breadcrumb else None
        category = category_tag.get_text(strip=True) if category_tag else "Unknown"

        # Ngày thu thập dữ liệu
        collected_date = datetime.now().strftime('%Y-%m-%d')

        # Kiểm tra và trả về các chi tiết của bài báo
        return {
            "title": title if title else "No Title",
            "url": article_url,
            "content": content if content else "No Content",
            "published_date": published_date if published_date else "Unknown",
            "author": author_info if author_info else "Unknown",
            "category": category if category else "Unknown",
            "collected_date": collected_date
        }

    def collect_articles_from_page(self, page_url):
        """Thu thập bài viết từ trang VNExpress"""
        page_html = self.fetch_html(page_url)
        if page_html is None:
            return [], None

        soup = BeautifulSoup(page_html, 'html.parser')
        article_tags = soup.find_all('h3') or soup.find_all('article')
        article_urls = []
        for tag in article_tags:
            link = tag.find('a', href=True)
            if link:
                href = link['href']
                if href.startswith('/'):
                    href = 'https://vnexpress.net' + href
                article_urls.append(href)

        next_page = soup.find('a', class_='next-page')
        next_page_url = next_page['href'] if next_page else None
        return article_urls, next_page_url

    def create_url_for_date(self, date):
        """Tạo URL theo ngày cho các danh mục trên VNExpress"""
        timestamp = self.date_to_timestamp(date)
        return [
            f'https://vnexpress.net/category/day/cateid/1005628/fromdate/{timestamp}/todate/{timestamp}/page/1',  # Bất động sản
            f'https://vnexpress.net/category/day/cateid/1003159/fromdate/{timestamp}/todate/{timestamp}/page/1',  # Kinh Doanh
            # f'https://vnexpress.net/category/day/cateid/1005628/fromdate/{timestamp}/todate/{timestamp}/page/1',  # Bất động sản
            f'https://vnexpress.net/category/day/cateid/1001002/fromdate/{timestamp}/todate/{timestamp}/page/1'   # Thế giới
        ]

    def collect_articles_between_dates(self, start_date, end_date):
        """Thu thập tất cả các bài viết trong khoảng thời gian"""
        all_articles = []
        current_date = start_date
        while current_date <= end_date:
            urls = self.create_url_for_date(current_date)
            print(f"Collecting articles for date: {current_date.strftime('%Y-%m-%d')}")
            for url in urls:
                article_urls, next_page_url = self.collect_articles_from_page(url)
                for article_url in article_urls:
                    article_details = self.extract_article_details(article_url)
                    if article_details:
                        all_articles.append(article_details)
            current_date += timedelta(days=1)
        return all_articles