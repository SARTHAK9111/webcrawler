from pathlib import Path
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import scrapy


class FormulaOneSpider(scrapy.Spider):
    name = "f1_crawler"
    allowed_domains = ["en.wikipedia.org"]
    custom_settings = {
        'DEPTH_LIMIT': 6,
        'MAX_PAGES': 300
    }

    def __init__(self, *args, **kwargs):
        super(FormulaOneSpider, self).__init__(*args, **kwargs)
        self.page_count = 0

    def start_requests(self):
        start_urls = ["https://en.wikipedia.org/wiki/Formula_One"]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if self.page_count >= self.custom_settings.get('MAX_PAGES'):
            self.logger.info(f"Reached maximum pages limit ({self.custom_settings.get('MAX_PAGES')}). Stopping crawl.")
            return
        page = response.url.split("/")[-1]
        filename = f"E:/IR/IRProject/Web_Crawler_Sarthak/f1_crawler/webpages/{page}.html"
        file_path = Path(f'{filename}')
        file_path.write_bytes(response.body)

        self.page_count += 1

        yield {
            "title": response.css("span.mw-page-title-main::text").get(),
            "paragraphs": "".join(response.css("div.mw-content-ltr p::text").getall()),
        }
        for link in response.css("div.mw-content-ltr p a::attr(href)").extract()[:5]:
            if link.startswith("/wiki/") and ':' not in link:
                nextPage = response.urljoin(link)
                yield scrapy.Request(nextPage, callback=self.parse)