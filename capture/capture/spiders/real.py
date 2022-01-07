import scrapy


class RealSpider(scrapy.Spider):
    name = 'real'
    allowed_domains = ['realtoon180.link']
    start_urls = ['http://realtoon180.link/']

    def parse(self, response):
        pass
