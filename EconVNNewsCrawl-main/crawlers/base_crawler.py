import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from http.client import IncompleteRead
from time import sleep

class BaseCrawler:
    def __init__(self):
        self.seen_urls = set()
        
    def fetch_html(self, url, retries=3, timeout=10):
        """Tải nội dung HTML từ một URL với số lần thử lại (retries) và thời gian timeout tùy chỉnh."""
        for attempt in range(retries):
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:11.0) Gecko/20100101'}
                request = urllib.request.Request(url, headers=headers)
                
                # Gửi request với thời gian timeout tùy chỉnh
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    return response.read()
            
            except IncompleteRead as e:
                print(f"IncompleteRead error for {url}: {e}. Attempt {attempt + 1} of {retries}")
                if attempt + 1 == retries:
                    print(f"Failed to fetch {url} after {retries} attempts.")
                    return None
                sleep(2)  # Thử lại sau 2 giây
            
            except Exception as e:
                print(f"Could not fetch URL {url}: {e}")
                return None


    def extract_article_details(self, article_url):
        """Lấy chi tiết bài báo, cần được ghi đè trong lớp con"""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def collect_articles_from_page(self, page_url):
        """Thu thập bài viết từ trang, cần được ghi đè trong lớp con"""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def create_url_for_date(self, date):
        """Tạo URL theo ngày, cần được ghi đè trong lớp con"""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def collect_articles_between_dates(self, start_date, end_date):
        """Thu thập tất cả các bài viết trong khoảng thời gian"""
        current_date = start_date
        all_articles = []
        while current_date <= end_date:
            urls = self.create_url_for_date(current_date)
            print(f"Collecting articles for date: {current_date.strftime('%Y-%m-%d')}")
            for url in urls:
                articles = self.collect_articles_from_page(url)
                all_articles.extend(articles)
            current_date += timedelta(days=1)
        return all_articles
