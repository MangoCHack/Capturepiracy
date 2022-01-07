import scrapy


class MangaSpider(scrapy.Spider):
    name = 'manga'
    allowed_domains = ['mangatoon139.com']
    start_urls = ['http://mangatoon139.com/']

    def parse(self, response):
        pass
