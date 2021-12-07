import scrapy


class NewtokiSpider(scrapy.Spider):
    name = 'newtoki'
    allowed_domains = ['newtoki95.com']
    start_urls = ['https://newtoki95.com/']

    def parse(self, response):
        pass
