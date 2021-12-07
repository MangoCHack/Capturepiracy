import scrapy


class NamedtoonSpider(scrapy.Spider):
    name = 'namedtoon'
    allowed_domains = ['namedtoon76.com']
    start_urls = ['https://namedtoon76.com/']

    def parse(self, response):
        pass
