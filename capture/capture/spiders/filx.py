import scrapy


class FilxSpider(scrapy.Spider):
    name = 'filx'
    allowed_domains = ['flix21.net']
    start_urls = ['http://flix21.net/']

    def parse(self, response):
        pass
