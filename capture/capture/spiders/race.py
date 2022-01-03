import scrapy
import datetime
from capture.items import WebtoonItem
import re

class RaceSpider(scrapy.Spider):
    name = 'race'
    #allowed_domains = ['www.race58.xyz']
    start_urls = ['https://www.race58.xyz/']

    def parse(self, response):
        '''
        for n, weekly in enumerate(response.xpath('/html/body/div[1]/div[3]/div/div/div[4]/div[3]/ul').xpath('//li').getall(),1):  #weekly page list
            webtoon_page = response.urljoin(weekly)
            yield scrapy.Request(webtoon_page, callback=self.webtoonList)
        '''
        webtoon_page='https://www.race58.xyz/'
        yield scrapy.Request(webtoon_page, callback=self.webtoonList)
         
    def webtoonList(self, response): #weekly webtoonList
        #webtoon_list = response.xpath('/html/body/div[7]/div/div[1]/div/div').xpath('//p/a').xpath('@href').getall()
        
        webtoon_list = response.css('.section-item-inner').getall()
        today = []
        for i in range(len(webtoon_list)):
            flag = re.findall(r'>업데이트 ',webtoon_list[i])
            url = re.findall(r'a href="(.+)"',webtoon_list[i])
            if len(flag) == 0:
                continue
            else:
                today.append(response.urljoin(url[0]))
        print(today)
        for n, webtoon in enumerate(today):
            yield scrapy.Request(webtoon, callback=self.webtoonPage)
        
    def webtoonPage(self, response): #웹툰 몇화 고르는 페이지 접근해서 데이터 추출
        item = WebtoonItem()
        
        webtoon = response.urljoin(response.css('.content__title').xpath('.//a').xpath('@href').get().strip())
        item['hosturl'] = response.url.split('/')[2]
        item['webtoonName'] = response.css('#wt_list > div:nth-child(4) > h1').xpath('text()').get().strip()
        item['updatetime'] = response.css('.content__title').xpath('.//span/text()').getall()
        now = datetime.datetime.now()
        item['crawltime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            item['episode'] = re.findall(r'([0-9]+)[화\.]',response.css('.content__title').xpath('.//a/text()').getall()[0].strip())[0]
        except IndexError:
            print('[-][-][-][-][-][-] IndexError')
            print(response.css('.content__title').xpath('.//a/text()').getall()[0].strip())
            item['episode'] = response.css('.content__title').xpath('.//a/text()').getall()[0].strip()
        yield scrapy.Request(webtoon, callback=self.webtoonCollect, meta={'webtoon':item})

    def webtoonCollect(self, response):
        item = response.meta.get('webtoon')
        #bo_v_con > img:nth-child(3)
        DownloadUrl = response.css('.contents').xpath('.//image').xpath('@src').getall()[0]
        #item['file_urls'] = [DownloadUrl] #download 할때는 list로 들어가야함
        item['file_urls'] = DownloadUrl #DB로 저장할때는 원본 그대로
        item['extension'] = DownloadUrl.split('.')[-1]
        yield item