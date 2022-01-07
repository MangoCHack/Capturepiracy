import scrapy


class CucuSpider(scrapy.Spider):
    name = 'cucu'
    allowed_domains = ['cucktoon129.com']
    start_urls = ['http://cucktoon129.com/']

    def parse(self, response):
        pass
