import scrapy


class TkrSpider(scrapy.Spider):
    name = 'tkr'
    allowed_domains = ['tkr071.com/']
    start_urls = ['http://tkr071.com//']

    def parse(self, response):
        pass
