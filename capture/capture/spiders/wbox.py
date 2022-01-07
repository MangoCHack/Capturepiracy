import scrapy


class WboxSpider(scrapy.Spider):
    name = 'wbox'
    allowed_domains = ['wtbox01.com']
    start_urls = ['http://wtbox01.com/']

    def parse(self, response):
        pass
