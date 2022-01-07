import scrapy


class KindSpider(scrapy.Spider):
    name = 'kind'
    allowed_domains = ['k1.kindtoon.com']
    start_urls = ['http://k1.kindtoon.com/']

    def parse(self, response):
        pass
