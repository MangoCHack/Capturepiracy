import scrapy


class SureSpider(scrapy.Spider):
    name = 'sure'
    allowed_domains = ['sure-02.link']
    start_urls = ['https://sure-02.link/']

    def parse(self, response):
        pass
