import scrapy
import datetime
from capture.items import WebtoonItem
import re


class FrtSpider(scrapy.Spider):
    name = 'frt'
    #allowed_domains = ['frt777.com']
    start_urls = ['https://frt777.com/']

    def parse(self, response):
        '''
        for n, weekly in enumerate(response.xpath('/html/body/div[1]/div[3]/div/div/div[4]/div[3]/ul').xpath('//li').getall(),1):  #weekly page list
            webtoon_page = response.urljoin(weekly)
            yield scrapy.Request(webtoon_page, callback=self.webtoonList)
        '''
        webtoon_page='https://frtoon89.com/toon/continue/week/9' #업데이트 웹툰페이지
        yield scrapy.Request(webtoon_page, callback=self.webtoonList)
         
    def webtoonList(self, response): #weekly webtoonList
        #webtoon_list = response.xpath('/html/body/div[7]/div/div[1]/div/div').xpath('//p/a').xpath('@href').getall()
        
        webtoon_list = response.xpath('/html/body/div[9]/div/div').getall()
        today = []
        for i in range(len(webtoon_list)):
            flag = re.findall(r'>(오늘)<',webtoon_list[i])
            url = re.findall(r'a href="((http[s]{0,1}:/){0,1}/(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"',webtoon_list[i])
            if len(flag) == 0:
                continue
            else:
                if url[0][0].find('http') != -1:#url에 따라 response.urljoin(url[0]) 필요
                    today.append(url[0][0]) 
                else:
                    today.append(response.urljoin(url[0][0]))
        
        for n, webtoon in enumerate(today):
            yield scrapy.Request(webtoon, callback=self.webtoonPage)
        
    def webtoonPage(self, response): #웹툰 몇화 고르는 페이지 접근해서 데이터 추출
        item = WebtoonItem()
        now = datetime.datetime.now()
        webtoon = response.xpath('/html/body/div[4]/div[2]/div/div/div[1]/div[2]/div/div/a/@href').get()
        item['hosturl'] = response.url.split('/')[2]
        item['webtoonName'] = response.xpath('/html/body/div[4]/div[1]/div/div/div/div/div[2]/p/text()').getall()[0].strip()
        item['updatetime'] = now.strftime('%Y-%m-%d %H:%M:%S') # update 시간이 안적혀 있음
        item['crawltime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            item['episode'] = re.findall(r'([0-9]+)[권회화\.]',response.xpath('/html/body/div[4]/div[2]/div/div/div[1]/div[2]/div/div/a/p/text()').get().strip())[0]
        except IndexError:
            print('[-][-][-][-][-][-] IndexError')
            print(response.xpath('/html/body/div[4]/div[2]/div/div/div[1]/div[2]/div/div/a/p/text()').get().strip())
            item['episode'] = response.xpath('/html/body/div[4]/div[2]/div/div/div[1]/div[2]/div/div/a/p/text()').get().strip()
        yield scrapy.Request(webtoon, callback=self.webtoonCollect, meta={'webtoon':item})

    def webtoonCollect(self, response):
        item = response.meta.get('webtoon')
        DownloadUrl = response.xpath('/html/body/div[7]/div/div/section/div[2]/img[1]/@src').get()
        #item['file_urls'] = [DownloadUrl] #download 할때는 list로 들어가야함
        item['file_urls'] = DownloadUrl #DB로 저장할때는 원본 그대로
        item['extension'] = DownloadUrl.split('.')[-1]
        yield item
