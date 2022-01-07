import scrapy


class CucciSpider(scrapy.Spider):
    name = 'cucci'
    allowed_domains = ['cuccitoon1.com']
    start_urls = ['http://cuccitoon1.com/']

    def parse(self, response):
        pass
