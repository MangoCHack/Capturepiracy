import scrapy
import datetime
from capture.items import WebtoonItem
import re
from scrapy_selenium import SeleniumRequest

class HoduSpider(scrapy.Spider): #javascript page loading
    name = 'hodu'
    #allowed_domains = ['hodu224.net']
    start_urls = ['https://hodu229.net/']

    def parse(self, response):
        '''
        for n, weekly in enumerate(response.xpath('/html/body/div[1]/div[3]/div/div/div[4]/div[3]/ul').xpath('//li').getall(),1):  #weekly page list
            webtoon_page = response.urljoin(weekly)
            yield scrapy.Request(webtoon_page, callback=self.webtoonList)
        '''
        webtoon_page='https://hodu229.net/toon' #업데이트 웹툰페이지
        
        yield SeleniumRequest(url=webtoon_page, callback=self.webtoonList)
         
    def webtoonList(self, response): #weekly webtoonList
        #webtoon_list = response.xpath('/html/body/div[7]/div/div[1]/div/div').xpath('//p/a').xpath('@href').getall()
        
        webtoon_list = response.css('.webtoon-list').xpath('.//li').getall()
        print(response.body)
        print(webtoon_list)
        '''
        today = []
        for i in range(len(webtoon_list)):
            
            flag = re.findall(r'>[\n](오늘) <',webtoon_list[i])
            url = re.findall(r'a href="((http[s]{0,1}:/){0,1}/(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=;]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"',webtoon_list[i])
            
            if len(flag) == 0:
                continue
            else:
                if url[0][0].find('http') < 0:#url에 따라 response.urljoin(url[0]) 필요
                    today.append(response.urljoin(url[0][0]))
                else:
                    today.append(url[0][0])
        
        for n, webtoon in enumerate(today):
            yield scrapy.Request(webtoon, callback=self.webtoonPage,cookies={'PHPSESSID':'hlrnt8k1368ek020gfn3m3krhq9ob49cjb4ubbmspcrk54gbab1mjs4f3sv89jce'})
        
    def webtoonPage(self, response): #웹툰 몇화 고르는 페이지 접근해서 데이터 추출
        #capta 있음.. 우회방법 찾아야함, 캡쳐 통과한 PHPSESSID를 cookie로 넘겨주면 통과할 수 있음. 유지시간
        item = WebtoonItem()
        now = datetime.datetime.now()
        webtoon = response.css('.list-item').xpath('.//div[2]/a/@href').get()
        if webtoon.find('http') < 0:
            webtoon = response.urljoin(webtoon)
        item['hosturl'] = response.url.split('/')[2]
        item['webtoonName'] = response.css('.view-content').xpath('.//span/b/text()').get().strip()
        item['updatetime'] = now.strftime('%Y-%m-%d ') + response.css('.list-item').xpath('.//div[4]/span/text()').get()
        item['crawltime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            item['episode'] = re.findall(r'([0-9]+)[화\.]',response.css('.list-item').xpath('.//div[2]/a/text()').getall()[1].strip())[0]
        except IndexError:
            print('[-][-][-][-][-][-] IndexError')
            print(response.css('.list-item').xpath('.//div[2]/a/text()').getall()[1].strip())
            item['episode'] = response.css('.list-item').xpath('.//div[2]/a/text()').getall()[1].strip()
        yield scrapy.Request(webtoon, callback=self.webtoonCollect,cookies={'PHPSESSID':'hlrnt8k1368ek020gfn3m3krhq9ob49cjb4ubbmspcrk54gbab1mjs4f3sv89jce'}, meta={'webtoon':item})

    def webtoonCollect(self, response):
        item = response.meta.get('webtoon')
        DownloadUrl = response.xpath('/html/body/div[1]/div/div/div[3]/div[2]/div/div/div[1]/section/article/div[3]/div/div[3]/img[1]/@src').get()
        #item['file_urls'] = [DownloadUrl] #download 할때는 list로 들어가야함
        item['file_urls'] = DownloadUrl #DB로 저장할때는 원본 그대로
        item['extension'] = DownloadUrl.split('.')[-1]
        yield item
    '''