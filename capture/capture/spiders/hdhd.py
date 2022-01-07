import scrapy


class HdhdSpider(scrapy.Spider):
    name = 'hdhd'
    allowed_domains = ['hdhd104.net/']
    start_urls = ['http://hdhd104.net//']

    def parse(self, response):
        pass
