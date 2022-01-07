import scrapy


class YayaSpider(scrapy.Spider):
    name = 'yaya'
    allowed_domains = ['yayaya133.com']
    start_urls = ['http://yayaya133.com/']

    def parse(self, response):
        pass
