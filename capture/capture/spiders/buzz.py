import scrapy


class BuzzSpider(scrapy.Spider):
    name = 'buzz'
    allowed_domains = ['buzztoon125.com/']
    start_urls = ['http://buzztoon125.com//']

    def parse(self, response):
        pass
