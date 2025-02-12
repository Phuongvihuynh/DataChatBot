
---

# EconVNNewsCrawl

## Overview

EconVNNewsCrawl is a powerful, customizable tool designed to scrape economic, financial, and business news from reputable Vietnamese news sources. The aim is to gather high-quality data for research, sentiment analysis, and natural language processing (NLP) applications. With a modular design, you can easily extend this crawler to other news sites and data sources.

### Key Features

- **Multiple Source Crawling:**

  - **Cafebiz.vn**: A leading source of business news in Vietnam, providing insights into the country's business landscape, entrepreneurship, and economic trends.
  - **Cafef.vn**: Renowned for its in-depth coverage of financial markets, stock analysis, and corporate financials, Cafef.vn is a top choice for economic data.
  - **VNExpress.net**: One of Vietnam's most reliable general news outlets, VNExpress covers global and local economics, business, and financial updates.
  - **Vietnamnet.vn**: Another leading Vietnamese news outlet known for its comprehensive coverage of economic and policy news, making it highly suitable for economic research and market tracking.
- **Extensibility**: The system is designed to add more news sources in the future without reworking the entire infrastructure. You can easily integrate other sources by creating additional crawlers using the base class.
- **Data Format**: All articles are saved in structured JSON format, with key fields such as title, content, author, published date, category, and URL.

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/EconVNNewsCrawl.git
   cd EconVNNewsCrawl
   ```
2. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Make sure you have a data directory to store crawled results:

   ```bash
   mkdir -p data
   ```

### Usage

Run the crawler by selecting the source and specifying the date range:

```bash
python main.py
```

You will be prompted to select a news source from the list:

1. Cafebiz
2. Cafef
3. VNExpress
4. Vietnamnet

Then, you will need to enter the start and end dates in the format `YYYY-MM-DD`. The program will scrape news articles within this date range and save the data in the `data/` directory.

### Example

```bash
Select the source to scrape:
1: Cafebiz
2: Cafef
3: VNExpress
4: Vietnamnet
Enter the number corresponding to the source (1, 2, 3, or 4): 3
Enter start date (YYYY-MM-DD): 2024-01-01
Enter end date (YYYY-MM-DD): 2024-01-05
```

The program will then scrape all available articles from VNExpress within the specified date range and save the result to a JSON file.

### Data Structure

Each JSON file generated will have the following structure:

```json
{
        "title": "Đầu năm 2024, nhiều ngân hàng giảm mạnh lãi suất huy động",
        "url": "https://cafebiz.vn/dau-nam-2024-nhieu-ngan-hang-giam-manh-lai-suat-huy-dong-176240101154611198.chn",
        "content": "Nhiều ngân hàng mới đây đã công bố biểu lãi suất huy động mới, hiệu lực những ngày giao dịch cuối năm 2023 hoặc đầu năm 2024.\nTạiSaigonbank, ngân hàng này áp dụng biểu lãi suất mới từ ngày 29/12/2023. Theo đó, lãi suất tiền gửi cao nhất tại nhà băng này chỉ còn 5,5%/năm, áp dụng cho khách hàng gửi tiền kỳ hạn từ 18 tháng trở lên, giảm 0,1 điểm % so với trước.\nĐặc biệt, lãi suất tiền gửi kỳ hạn 13 tháng tại Saigonbank giảm mạnh từ 5,8%/năm xuống còn 5,3%/năm. Lãi suất kỳ hạn 12 tháng cũng giảm sâu từ 5,4%/năm xuống còn 5,1%/năm.\nỞ các kỳ hạn ngắn, Saigonbank cũng điều chỉnh khoảng điểm %. Cụ thể ở kỳ hạn gửi 6 tháng, lãi suất giảm 0,7 điểm % xuống còn 4,2%/năm. Lãi suất kỳ hạn 3 tháng giảm 0,5 điểm % xuống 3%/năm.\nNgay trước kỳ nghỉ lễ Tết Dương lịch,Techcombankcũng áp dụng biểu lãi suất huy động mới dành cho khách hàng cá nhân từ ngày 27/12/2023. Theo đó, lãi suất kỳ hạn gửi 12 tháng trở lên tại ngân hàng này chỉ còn 4,75 – 5%/năm. Trong đó, lãi suất cao nhất 5%/năm dành cho khách hàng Private gửi số tiền từ 3 tỷ đồng.\nLãi suất kỳ hạn 6 tháng của Techcombank cũng đã điều chỉnh xuống mức 4,35-4,6%/năm. Lãi suất kỳ hạn 3 tháng là 3,35-3,5%/năm.\nVietinBankvừa qua cũng thay đổi biểu lãi suất huy động từ ngày 27/12 với việc điều chỉnh giảm 0,4-0,5%/năm ở các kỳ hạn dưới 12 tháng. Theo đó, mức lãi suất áp dụng cho các kỳ hạn từ 1 tháng đến dưới 3 tháng giảm từ 2,6%/năm xuống 2,2%/năm; kỳ hạn từ 3 đến dưới 6 tháng giảm từ 3%/năm xuống còn 2,5%/năm; kỳ hạn từ 6 tháng đến dưới 12 tháng giảm từ 4%/năm xuống còn 3,5%/năm.\nLãi suất huy động các kỳ hạn từ 12 tháng đến dưới 24 tháng vẫn được giữ nguyên ở mức 5%/năm. Đồng thời, các kỳ hạn từ 24 tháng trở lên cũng tiếp tục được hưởng lãi suất cao nhất là 5,3%/năm.\nĐây là lần giảm lãi suất thứ hai của VietinBank trong chưa đầy nửa tháng qua. Trước đó, ngân hàng này cũng đã giảm 0,3 – 0,4 điểm % lãi suất huy động tại các kỳ hạn dưới 13 tháng và giữ nguyên tại các kỳ hạn dài.\nABBankcũng điều chỉnh lãi suất từ ngày 27/12/2023. Trong đó, lãi suất kỳ hạn 13 tháng – 36 tháng giảm mạnh từ 4,4%/năm xuống còn 4%/năm. Lãi suất kỳ hạn 48 tháng và 60 tháng cũng giảm 0,4 điểm % xuống 3,6%/năm.\nLãi suất cao nhất của nhà băng này là 5,3%/năm, áp dụng cho kỳ hạn 6 tháng, bất ngờ tăng 0,4 điểm % so với đầu tháng 12/2023. Lãi suất kỳ hạn 7 tháng và 8 tháng giảm 0,2 điểm % xuống 5%/năm.\nABBank có biểu niêm yết lãi suất với quy luật khác so với các ngân hàng khác. Hiện những kỳ hạn ngắn tại ABBank như 6 tháng – 8 tháng mới có mức lãi suất cao nhất. Trong khi đó, các kỳ hạn dài tại ABBank có lãi suất thấp hơn nhiều.\nTheo giới chuyên gia, tăng trưởng huy động vốn của hệ thống ngân hàng năm 2023 ở mức cao hơn so với các năm trước bất chấp việc lãi suất tiền gửi xuống thấp kỷ lục. Điều này cũng cho thấy tâm lý e ngại của người dân trong bối cảnh nền kinh tế nhiều khó khăn, các kênh đầu tư nhiều rủi ro và kém sôi động. Thay vì rót tiền vào bất động sản, đầu tư chứng khoán, trái phiếu doanh nghiệp, người dân vẫn ưa chuộng gửi tiền ngân hàng như một kênh đảm bảo an toàn nguồn vốn.\nMinh Vy",
        "published_date": "01/01/2024 15:46 PM",
        "author_info": "Minh Vy",
        "category": "Kinh tế vĩ mô",
        "collected_date": "2024-10-10"
    },
```

### Sources and Data Quality

1. **Cafebiz.vn**: Popular among the Vietnamese business community for reliable news on entrepreneurship, market trends, and corporate affairs.
2. **Cafef.vn**: Known for its financial analysis, Cafef is a go-to source for anyone researching the Vietnamese stock market and financial reports.
3. **VNExpress.net**: A reputable news site covering a broad range of topics. It has a strong focus on domestic and global business news and offers valuable insights into Vietnam’s economic policies and trends.
4. **Vietnamnet.vn**: Provides up-to-date news on policies, macroeconomics, and international trade, making it an excellent resource for economic research.

These sources are well-regarded in Vietnam for their accuracy and in-depth reporting. They offer a robust dataset for anyone studying Vietnam's economy, business, or financial markets. The crawled data can be used for a variety of purposes, including trend analysis, sentiment analysis, and NLP tasks.

### Future Updates

- **More News Sources**: Future versions may include additional reputable Vietnamese news outlets like **Bao Moi**, **Thanh Nien**, and **Tuoi Tre**.
- **Enhanced Error Handling**: Improve the retry logic and error-handling mechanisms to minimize incomplete or failed data collection.
- **Data Enrichment**: In future versions, crawled articles may include metadata such as stock tickers or company names to help identify relevant financial data.
- **Pagination Support**: Currently, pagination for certain news sites is not fully supported. Future updates will address this limitation, ensuring that all available articles are fetched.

### License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

### Contributions

Feel free to fork the repository, submit pull requests, or open issues for any improvements or bugs you encounter. This project is a collaborative effort, and we welcome contributions that make it even more robust and versatile.
