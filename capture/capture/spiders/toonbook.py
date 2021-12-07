import scrapy


class ToonbookSpider(scrapy.Spider):
    name = 'toonbook'
    allowed_domains = ['toonbook.net']
    start_urls = ['https://toonbook.net/']

    def parse(self, response):
        pass
