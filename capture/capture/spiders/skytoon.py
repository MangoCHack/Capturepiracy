import scrapy
import datetime
from capture.items import WebtoonItem
import re
from scrapy_selenium import SeleniumRequest

class SkytoonSpider(scrapy.Spider):
    name = 'skytoon'
    #allowed_domains= ['www.skytoon12.com/webtoon']
    start_urls = ['https://www.skytoon16.com/webtoon/']

    def parse(self, response):
        '''
        for n, weekly in enumerate(response.xpath('/html/body/div[1]/div[3]/div/div/div[4]/div[3]/ul').xpath('//li').getall(),1):  #weekly page list
            webtoon_page = response.urljoin(weekly)
            yield scrapy.Request(webtoon_page, callback=self.webtoonList)
        '''
        webtoon_page='https://www.skytoon16.com/webtoon/'
        yield scrapy.Request(webtoon_page, callback=self.webtoonList)
         
    def webtoonList(self, response): #weekly webtoonList        
        webtoon_list = response.css('body > div:nth-child(6) > div > div.list > ul > li.new').getall() #업데이트 된것 li class new
        if response.meta.get('page_num') is not None:
            page_num = response.meta.get('page_num')
        else:
            page_num = 1
        today = []
        for i in range(len(webtoon_list)):
            url = re.findall(r'a href="(.+)"',webtoon_list[i])
            today.append(response.urljoin(url[0]))
        
        for n, webtoon in enumerate(today):
            yield SeleniumRequest(url=webtoon, callback=self.webtoonPage)
        
        if len(today) != 0:
            page_num += 1
            next_page = f"https://www.skytoon16.com/webtoon/index/0?&page={page_num}"
            yield scrapy.Request(next_page, callback=self.webtoonList, meta={'page_num':page_num})
        

        
    def webtoonPage(self, response): #웹툰 몇화 고르는 페이지 접근해서 데이터 추출
        item = WebtoonItem()
        
        item['hosturl'] = response.url.split('/')[2]
        item['webtoonName'] = response.css('body > div.play > div > div.topbottom > div > p.tit').xpath('text()').get().strip()
        now = datetime.datetime.now()
        item['crawltime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        item['updatetime'] = now.strftime('%Y-%m-%d %H:%M:%S') #update 시간 따로 안 적혀있음
        try:
            item['episode'] = re.findall(r'([0-9]+)[권회화\.]',response.css('body > div.play > div > div.topbottom > div > div.btn_list > p').xpath('.//text()').getall()[0].strip())[0]
        except IndexError:
            print('[-][-][-][-][-][-] IndexError')
            print(response.css('body > div.play > div > div.topbottom > div > div.btn_list > p').xpath('.//text()').getall()[0].strip())
            item['episode'] = response.css('body > div.play > div > div.topbottom > div > div.btn_list > p').xpath('.//text()').getall()[0].strip()

        #회차 선택하는것 없음. 바로 최신 회차로 이동, 동적로딩필요
        DownloadUrl = response.css('.lazy').xpath('@data-src').getall()[0]
        print(DownloadUrl)
        item['file_urls'] = DownloadUrl.strip() #DB로 저장할때는 원본 그대로
        item['extension'] = DownloadUrl.split('.')[-1].strip()
        yield item