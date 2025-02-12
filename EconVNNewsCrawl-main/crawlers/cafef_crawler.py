from crawlers.base_crawler import BaseCrawler
from bs4 import BeautifulSoup
from datetime import datetime

class CafefCrawler(BaseCrawler):
    def extract_article_details(self, article_url):
        """Lấy chi tiết bài báo từ URL bài báo của Cafef"""
        article_html = self.fetch_html(article_url)
        if article_html is None:
            return None

        soup = BeautifulSoup(article_html, 'html.parser')

        # Lấy tiêu đề bài báo
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else None

        # Lấy phần sapo
        sapo = soup.find('h2', class_='sapo')
        content_sapo = sapo.get_text(strip=True) if sapo else ""

        # Lấy nội dung từ <div class="detail-content">
        detail_content = soup.find('div', class_='detail-content')
        content_paragraphs = detail_content.find_all('p') if detail_content else []
        content_body = "\n".join([para.get_text(strip=True) for para in content_paragraphs])

        content = content_sapo + "\n" + content_body if content_body else content_sapo

        # Lấy ngày đăng bài từ <span class="pdate">
        time_span = soup.find('span', class_='pdate')
        published_date = time_span.get_text(strip=True) if time_span else None

        # Lấy tác giả từ <p class="author">
        author_info = soup.find('p', class_='author')
        author = author_info.get_text(strip=True) if author_info else "Unknown"

        # Lấy chuyên mục từ <a class="category-page__name cat">
        category_tag = soup.find('a', {'data-role': 'cate-name', 'class': 'category-page__name cat'})
        category = category_tag.get_text(strip=True) if category_tag else "Unknown"

        # Ngày thu thập dữ liệu
        collected_date = datetime.now().strftime('%Y-%m-%d')

        return {
            "title": title,
            "url": article_url,
            "content": content.strip(),
            "published_date": published_date,
            "author": author,
            "category": category,
            "collected_date": collected_date
        }

    def collect_articles_from_page(self, page_url):
        """Thu thập tất cả các bài viết từ một trang"""
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
                title = link.get('title')
                if title and len(title.split()) >= 6:
                    full_url = 'https://cafef.vn' + href if href.startswith('/') else href
                    if full_url not in self.seen_urls:
                        article_details = self.extract_article_details(full_url)
                        if article_details:
                            article_data.append(article_details)
                        self.seen_urls.add(full_url)
        return article_data

    def create_url_for_date(self, date):
        """Tạo danh sách URL theo ngày cho trang Cafef"""
        date_str = date.strftime("%-d/%-m/%Y")
        return [
            f"https://cafef.vn/tai-chinh-ngan-hang/{date_str}.chn",
            f"https://cafef.vn/xa-hoi/{date_str}.chn",
            f"https://cafef.vn/thi-truong-chung-khoan/{date_str}.chn",
            f"https://cafef.vn/bat-dong-san/{date_str}.chn",
            f"https://cafef.vn/doanh-nghiep/{date_str}.chn",
            f"https://cafef.vn/smart-money/{date_str}.chn",
            f"https://cafef.vn/tai-chinh-quoc-te/{date_str}.chn",
            f"https://cafef.vn/vi-mo-dau-tu/{date_str}.chn",
            f"https://cafef.vn/kinh-te-so/{date_str}.chn",
            f"https://cafef.vn/thi-truong/{date_str}.chn"
        ]