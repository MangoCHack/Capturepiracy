import scrapy


class JamicsSpider(scrapy.Spider):
    name = 'jamics'
    allowed_domains = ['jamics.work']
    start_urls = ['http://jamics.work/']

    def parse(self, response):
        pass
