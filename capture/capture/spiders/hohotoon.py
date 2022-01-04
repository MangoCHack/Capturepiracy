import scrapy
import re
from urllib.parse import urlparse
from capture.items import WebtoonItem
import datetime
import time

class HohotoonSpider(scrapy.Spider):#캡챠있음
    name = 'hohotoon'
    #allowed_domains = ['hohotoon24.com']
    start_urls = ['https://hohotoon24.com/webtoon?toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0','https://hohotoon24.com/webtoon?toon=%EC%84%B1%EC%9D%B8%EC%9B%B9%ED%88%B0' ]

    def parse(self, response):
        '''
        for n, weekly in enumerate(response.xpath('/html/body/div[1]/div[3]/div/div/div[4]/div[3]/ul').xpath('//li').getall(),1):  #weekly page list
            webtoon_page = response.urljoin(weekly)
            yield scrapy.Request(webtoon_page, callback=self.webtoonList)
        '''

        yield scrapy.Request(response.url, callback=self.webtoonList)
         
    def webtoonList(self, response): #weekly webtoonList
        #webtoon_list = response.xpath('/html/body/div[7]/div/div[1]/div/div').xpath('//p/a').xpath('@href').getall()
        
        webtoon_list = response.css('.list').xpath('.//li').getall()
        
        for i in range(len(webtoon_list)):
            
            flag = re.findall(r'>[\n](오늘) <',webtoon_list[i])
            url = re.findall(r'a href="((http[s]{0,1}:/){0,1}/(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=;]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"',webtoon_list[i])
            _t = re.findall(r'date-update="([0-9]+)"',webtoon_list[i])[0]
            if len(flag) == 0:
                continue
            else:
                if url[0][0].find('http') < 0:#url에 따라 response.urljoin(url[0]) 필요
                    webtoon = response.urljoin(url[0][0])
                else:
                    webtoon = url[0][0]
            time.sleep(2)
            yield scrapy.Request(webtoon, callback=self.webtoonPage,cookies={'PHPSESSID':'hlrnt8k1368ek020gfn3m3krhq9ob49cjb4ubbmspcrk54gbab1mjs4f3sv89jce'},meta={'time':_t})
        
        
    def webtoonPage(self, response): #웹툰 몇화 고르는 페이지 접근해서 데이터 추출
        #capta 있음.. 캡챠 통과한 PHPSESSID를 cookie로 넘겨주면 통과할 수 있음. 유지시간은 모름
        #crawling 시작하면 ip 차단함 -> 최대한 천천히 수집
        item = WebtoonItem()
        now = datetime.datetime.now()
        
        webtoon = response.css('.list-item').xpath('.//div[2]/a/@href').get()
        if webtoon.find('http') < 0:
            webtoon = response.urljoin(webtoon)
        item['hosturl'] = response.url.split('/')[2]
        item['webtoonName'] = response.css('.view-content').xpath('.//span/b/text()').get().strip()
        item['updatetime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(response.meta.get('time'))))
        item['crawltime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            item['episode'] = re.findall(r'([0-9]+)[권회화\.]',response.css('.list-item').xpath('.//div[2]/a/text()').getall()[1].strip())[0]
        except IndexError:
            print('[-][-][-][-][-][-] IndexError')
            print(response.css('.list-item').xpath('.//div[2]/a/text()').getall()[1].strip())
            item['episode'] = response.css('.list-item').xpath('.//div[2]/a/text()').getall()[1].strip()
        yield item
        #selenium 적용 후 image url 수집 가능
        #yield scrapy.Request(webtoon, callback=self.webtoonCollect,cookies={'PHPSESSID':'hlrnt8k1368ek020gfn3m3krhq9ob49cjb4ubbmspcrk54gbab1mjs4f3sv89jce'}, meta={'webtoon':item})

    def webtoonCollect(self, response):
        item = response.meta.get('webtoon')
        #javascript rendering 필요/ src등 동적 생성 webdriver 필요
        DownloadUrl = response.xpath('/html/body/div[1]/div/div/div[3]/div[2]/div/div/div[1]/section/article/div[3]/div/div[3]/img[1]/@src').get()
        #item['file_urls'] = [DownloadUrl] #download 할때는 list로 들어가야함
        item['file_urls'] = DownloadUrl #DB로 저장할때는 원본 그대로
        print(DownloadUrl)
        item['extension'] = DownloadUrl.split('.')[-1]
        yield item