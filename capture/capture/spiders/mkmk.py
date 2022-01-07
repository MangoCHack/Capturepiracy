import scrapy


class MkmkSpider(scrapy.Spider):
    name = 'mkmk'
    allowed_domains = ['mkmk14.link']
    start_urls = ['http://mkmk14.link/']

    def parse(self, response):
        pass
