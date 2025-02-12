from crawlers.base_crawler import BaseCrawler
from bs4 import BeautifulSoup
from datetime import datetime

class CafebizCrawler(BaseCrawler):
    def extract_article_details(self, article_url):
        article_html = self.fetch_html(article_url)
        if article_html is None:
            return None

        soup = BeautifulSoup(article_html, 'html.parser')

        # Lấy các chi tiết bài báo
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else None
        sapo = soup.find('h2', class_='sapo')
        content_sapo = sapo.get_text(strip=True) if sapo else ""
        detail_content = soup.find('div', class_='detail-content')
        content_paragraphs = detail_content.find_all('p') if detail_content else []
        content_body = "\n".join([para.get_text(strip=True) for para in content_paragraphs])
        content = content_sapo + "\n" + content_body if content_body else content_sapo

        time_span = soup.find('span', class_='time')
        published_date = time_span.get_text(strip=True) if time_span else None
        author_info = soup.find('strong', class_='detail-author')
        author_info = author_info.get_text(strip=True) if author_info else "Unknown"
        category_tag = soup.find('span', class_='cat')
        category = category_tag.get_text(strip=True) if category_tag else "Unknown"

        collected_date = datetime.now().strftime('%Y-%m-%d')

        return {
            "title": title,
            "url": article_url,
            "content": content.strip(),
            "published_date": published_date,
            "author_info": author_info,
            "category": category,
            "collected_date": collected_date
        }

    def collect_articles_from_page(self, page_url):
        page_html = self.fetch_html(page_url)
        if page_html is None:
            return []

        soup = BeautifulSoup(page_html, 'html.parser')
        article_tags = soup.find_all('div', class_='item')

        article_data = []
        for tag in article_tags:
            link = tag.find('a', href=True)
            if link:
                href = link['href']
                title = link.get('title')
                if title and len(title.split()) >= 2:
                    full_url = 'https://cafebiz.vn' + href if href.startswith('/') else href
                    if full_url not in self.seen_urls:
                        article_details = self.extract_article_details(full_url)
                        if article_details:
                            article_data.append(article_details)
                        self.seen_urls.add(full_url)
        return article_data

    def create_url_for_date(self, date):
        date_str = date.strftime("%d-%m-%Y")
        return [
            f"https://cafebiz.vn/xem-theo-ngay-c176114-{date_str}.chn",
            f"https://cafebiz.vn/xem-theo-ngay-c176135-{date_str}.chn",
            f"https://cafebiz.vn/xem-theo-ngay-c176127-{date_str}.chn"
        ]
