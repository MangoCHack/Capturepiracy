import scrapy


class ToonsarangSpider(scrapy.Spider):
    name = 'toonsarang'
    allowed_domains = ['toonsarang.buzz']
    start_urls = ['https://toonsarang.buzz/']

    def parse(self, response):
        pass
