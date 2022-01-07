import scrapy


class StoonSpider(scrapy.Spider):
    name = 'stoon'
    allowed_domains = ['stoon1.com']
    start_urls = ['http://stoon1.com/']

    def parse(self, response):
        pass
