import scrapy


class ItflixSpider(scrapy.Spider):
    name = 'itflix'
    allowed_domains = ['www.it-flix.com']
    start_urls = ['https://www.it-flix.com/']

    def parse(self, response):
        pass
