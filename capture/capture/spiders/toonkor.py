import scrapy

class ToonkorSpider(scrapy.Spider):
    name = 'toonkor'
    allowed_domains = ['tkor.toys']
    start_urls = ['https://tkor.toys/']

    def parse(self, response):        
        for n, weekly in enumerate(response.xpath('/html/body/div[2]/div/div[1]/div[3]/div[1]/div[2]/div/ul').getall(),1):
            weeklyContents = scrapy.Selector(text=weekly)
            for m, one in enumerate(weeklyContents.xpath('//li/div/a').xpath('@href').getall(),1):
                webtoon_page = response.urljoin(one)
                print(webtoon_page)
        print('---------------------------------------------------')
        #'/html/body/div[2]/div/div[1]/div[3]/div[1]/div[2]/div/ul[1]' #월별 웹툰 리스트 ul[i]
        #//li[2]/div/a
        pass

    #def webtoon(self, response):

'''
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
'''