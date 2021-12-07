import scrapy


class RaceSpider(scrapy.Spider):
    name = 'race'
    allowed_domains = ['www.race58.xyz']
    start_urls = ['https://www.race58.xyz/']

    def parse(self, response):
        pass
