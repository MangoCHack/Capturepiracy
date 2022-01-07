import scrapy


class ShowmeSpider(scrapy.Spider):
    name = 'showme'
    allowed_domains = ['showme-34.com']
    start_urls = ['http://showme-34.com/']

    def parse(self, response):
        pass
