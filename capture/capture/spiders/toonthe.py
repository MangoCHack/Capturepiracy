import scrapy


class ToontheSpider(scrapy.Spider):
    name = 'toonthe'
    allowed_domains = ['v4.toonthe.com']
    start_urls = ['https://v4.toonthe.com/']

    def parse(self, response):
        pass
