import scrapy


class BlacktoonSpider(scrapy.Spider):
    name = 'blacktoon'
    #allowed_domains = ['blacktoon132.com']
    start_urls = ['https://blacktoon132.com/']

    def parse(self, response):
        pass
