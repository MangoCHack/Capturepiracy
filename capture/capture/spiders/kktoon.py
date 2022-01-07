import scrapy


class KktoonSpider(scrapy.Spider):
    name = 'kktoon'
    allowed_domains = ['kktoon50.com/']
    start_urls = ['http://kktoon50.com//']

    def parse(self, response):
        pass
