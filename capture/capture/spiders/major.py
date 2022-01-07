import scrapy


class MajorSpider(scrapy.Spider):
    name = 'major'
    allowed_domains = ['major-toon.com']
    start_urls = ['http://major-toon.com/']

    def parse(self, response):
        pass
