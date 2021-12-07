import scrapy


class WtwtSpider(scrapy.Spider):
    name = 'wtwt'
    allowed_domains = ['wtwt106.com']
    start_urls = ['https://wtwt106.com/']

    def parse(self, response):
        
        pass
