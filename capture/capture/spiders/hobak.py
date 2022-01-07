import scrapy


class HobakSpider(scrapy.Spider):
    name = 'hobak'
    allowed_domains = ['hobak101.com']
    start_urls = ['http://hobak101.com/']

    def parse(self, response):
        pass
