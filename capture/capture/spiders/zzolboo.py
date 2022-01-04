import scrapy
import datetime
from capture.items import WebtoonItem
import re

class SureSpider(scrapy.Spider):
    name = 'zzolboo'
    #allowed_domains = ['https://zzolboo90.com/toon/continue/week/9']
    start_urls = ['https://zzolboo90.com/']

    def parse(self, response):
        webtoon_page='https://zzolboo90.com/toon/continue/week/9'
        yield scrapy.Request(webtoon_page, callback=self.webtoonList)
         
    def webtoonList(self, response): #weekly webtoonList
        #webtoon_list = response.xpath('/html/body/div[7]/div/div[1]/div/div').xpath('//p/a').xpath('@href').getall()
        webtoon_list = response.css('.card').getall()
        today = []
        for i in range(len(webtoon_list)):
            flag = re.findall(r'>오늘<',webtoon_list[i])
            url = re.findall(r'a href="(.+?)"',webtoon_list[i])
            if len(flag) == 0:
                continue
            else:
                today.append(response.urljoin(url[0]))
        print(today)
        for n, webtoon in enumerate(today):
            yield scrapy.Request(webtoon, callback=self.webtoonPage)
        
    def webtoonPage(self, response): #웹툰 몇화 고르는 페이지 접근해서 데이터 추출
        item = WebtoonItem()
        
        webtoon = response.urljoin(response.css('.card-body').xpath('./a/@href').get())
        item['hosturl'] = response.url.split('/')[2]
        item['webtoonName'] = response.css('.card-text').xpath('./text()').get().strip()
        item['updatetime'] = response.css('.card-text').xpath('./span/text()').get()
        now = datetime.datetime.now()
        item['crawltime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            item['episode'] = re.findall(r'([0-9]+)[권회화\.]',response.css('.card-body').xpath('./a/p/text()').get().strip())[0]
        except IndexError:
            print('[-][-][-][-][-][-] IndexError')
            print(response.css('.card-body').xpath('./a/p/text()').get().strip())
            item['episode'] = response.css('.card-body').xpath('./a/p/text()').get().strip()
        yield scrapy.Request(webtoon, callback=self.webtoonCollect, meta={'webtoon':item})

    def webtoonCollect(self, response):
        item = response.meta.get('webtoon')
        
        DownloadUrl = response.css('.row').xpath('./div/section/div/img/@src').get()  #배너 수에 따라 xpath 달라질 수 있음 
        #item['file_urls'] = [DownloadUrl] #download 할때는 list로 들어가야함
        item['file_urls'] = DownloadUrl #DB로 저장할때는 원본 그대로
        item['extension'] = DownloadUrl.split('.')[-1]
        yield item
         