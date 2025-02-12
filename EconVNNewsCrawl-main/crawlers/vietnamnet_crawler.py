import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class VietnamnetCrawler:
    def __init__(self):
        self.base_url = "https://vietnamnet.vn"
        self.seen_urls = set()

    def fetch_html(self, url):
        """Lấy HTML từ URL"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:11.0) Gecko/20100101'}
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            return response.read()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def extract_article_details(self, article_url):
        """Lấy chi tiết bài viết từ URL"""
        if article_url in self.seen_urls:
            print(f"Duplicate article: {article_url}")
            return None

        article_html = self.fetch_html(article_url)
        if article_html is None:
            return None

        soup = BeautifulSoup(article_html, 'html.parser')

        # Lấy tiêu đề
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else None

        # Lấy nội dung từ <h2> và <div class="maincontent main-content">
        sapo = soup.find('h2', class_='content-detail-sapo sm-sapo-mb-0')
        content_sapo = sapo.get_text(strip=True) if sapo else ""

        main_content = soup.find('div', class_='maincontent main-content')
        content_paragraphs = main_content.find_all('p') if main_content else []
        content_body = "\n".join([para.get_text(strip=True) for para in content_paragraphs])

        content = content_sapo + "\n" + content_body if content_body else content_sapo

        # Lấy ngày đăng bài từ <div class="bread-crumb-detail__time">
        time_div = soup.find('div', class_='bread-crumb-detail__time')
        published_date = time_div.get_text(strip=True) if time_div else None

        # Lấy tên tác giả từ <div class="article-detail-author__main">
        author_wrapper = soup.find('div', class_='article-detail-author__main')
        author = "Unknown"
        if author_wrapper:
            author_tag = author_wrapper.find('a', {'title': True})
            if author_tag:
                author = author_tag['title']

        # Lấy category từ <div class="bread-crumb-detail">
        breadcrumb = soup.find('div', class_='bread-crumb-detail')
        category_tags = breadcrumb.find_all('li') if breadcrumb else []
        category = category_tags[-1].get_text(strip=True) if category_tags else "Unknown"

        # Ngày thu thập dữ liệu
        collected_date = datetime.now().strftime('%Y-%m-%d')

        # Đánh dấu URL đã thu thập
        self.seen_urls.add(article_url)

        return {
            "title": title if title else "No Title",
            "url": article_url,
            "content": content if content else "No Content",
            "published_date": published_date if published_date else "Unknown",
            "author": author if author else "Unknown",
            "category": category if category else "Unknown",
            "collected_date": collected_date
        }

    def collect_articles_from_page(self, page_url):
        """Thu thập bài viết từ trang"""
        page_html = self.fetch_html(page_url)
        if page_html is None:
            return []

        soup = BeautifulSoup(page_html, 'html.parser')

        # Tìm tất cả các thẻ <h3> chứa link bài báo
        article_tags = soup.find_all('h3')
        article_data = []

        for tag in article_tags:
            link = tag.find('a', href=True)
            if link:
                href = link['href']
                title = link.get('title')  # Extract title from 'title' attribute

                # Kiểm tra số từ trong tiêu đề (ít nhất 6 từ)
                if title and len(title.split()) >= 6:
                    if href.startswith('/'):
                        href = self.base_url + href  # Build full URL
                    article_details = self.extract_article_details(href)
                    if article_details:
                        article_data.append(article_details)

        return article_data

    def create_url_for_date(self, date):
        """Tạo URL theo ngày cho Vietnamnet"""
        date_str = date.strftime("%d/%m/%Y")
        encoded_date_str = date_str.replace("/", "%2F")
        return f"{self.base_url}/tin-tuc-24h?bydate={encoded_date_str}-{encoded_date_str}&cate=000003"

    def collect_articles_between_dates(self, start_date, end_date):
        """Thu thập bài viết trong khoảng thời gian"""
        current_date = start_date
        all_articles = []

        while current_date <= end_date:
            url = self.create_url_for_date(current_date)
            print(f"Collecting articles for date: {current_date.strftime('%d-%m-%Y')}")
            articles = self.collect_articles_from_page(url)
            all_articles.extend(articles)
            current_date += timedelta(days=1)

        return all_articles
