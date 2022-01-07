import scrapy


class AllallSpider(scrapy.Spider):
    name = 'allall'
    allowed_domains = ['www.allall47.net']
    start_urls = ['http://www.allall47.net/']

    def parse(self, response):
        pass
