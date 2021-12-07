import scrapy


class StarSpider(scrapy.Spider):
    name = 'star'
    allowed_domains = ['star-02.link']
    start_urls = ['https://star-02.link/']

    def parse(self, response):
        pass
