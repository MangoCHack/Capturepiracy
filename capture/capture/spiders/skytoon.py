import scrapy


class SkytoonSpider(scrapy.Spider):
    name = 'skytoon'
    allowed_domains = ['www.skytoon12.com/webtoon']
    start_urls = ['https://www.skytoon12.com/webtoon/']

    def parse(self, response):
        pass
