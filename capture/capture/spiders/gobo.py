import scrapy


class GoboSpider(scrapy.Spider):
    name = 'gobo'
    allowed_domains = ['gobotoon02.com']
    start_urls = ['http://gobotoon02.com/']

    def parse(self, response):
        pass
