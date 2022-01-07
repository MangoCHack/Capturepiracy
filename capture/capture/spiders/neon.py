import scrapy


class NeonSpider(scrapy.Spider):
    name = 'neon'
    allowed_domains = ['neonon1.com']
    start_urls = ['http://neonon1.com/']

    def parse(self, response):
        pass
