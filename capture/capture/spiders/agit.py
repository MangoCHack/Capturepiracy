import scrapy
import re
from urllib.parse import urlparse
from capture.items import WebtoonItem
import datetime

class AgitSpider(scrapy.Spider):
    name = 'agit'
    #allowed_domains = ['agit113.com']
    start_urls = ['https://agit113.com/']

    def parse(self, response):
        
        '''
        for n, weekly in enumerate(response.xpath('/html/body/div[3]/div/div/a').xpath('@href').getall(),1):  #weekly page list
            webtoon_page = response.urljoin(weekly)
            yield scrapy.Request(webtoon_page, callback=self.webtoonList,meta={'webtoon':item})
        '''
        webtoon_page='https://agit113.com/' #최신 업데이트 웹툰페이지
        yield scrapy.Request(webtoon_page, callback=self.webtoonList)
         
    def webtoonList(self, response): #weekly webtoonList
        #webtoon_list = response.xpath('/html/body/div[7]/div/div[1]/div/div').xpath('//p/a').xpath('@href').getall()
        
        webtoon_list = response.xpath('/html/body/div[4]/div[2]/div').getall()
        today = []
        for i in range(len(webtoon_list)):
            flag = re.findall(r'>(UP)<',webtoon_list[i])
            url = re.findall(r'a href="(/(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"',webtoon_list[i])
            print(flag,url)
            if len(flag) == 0:
                continue
            else:
                today.append(response.urljoin(url[0]))
        
        for n, webtoon in enumerate(today):
            yield scrapy.Request(webtoon, callback=self.webtoonPage)
        
    def webtoonPage(self, response): #웹툰 몇화 고르는 페이지 접근해서 데이터 추출
        item = WebtoonItem()
        webtoon = response.xpath('/html/body/div[2]/div[2]/div/div[2]/div/div/a').xpath('@href').getall()[0]
        item['hosturl'] = response.url.split('/')[2]
        item['webtoonName'] = response.xpath('/html/body/div[2]/div/div[2]/h3/text()').get().strip()
        item['updatetime'] = response.xpath('/html/body/div[5]/div/div/div/div[1]/a/div/p/span/i/text()').get().strip()
        now = datetime.datetime.now()
        item['crawltime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            item['episode'] = re.findall(r'([0-9]+)[화\.]',response.xpath('/html/body/div[5]/div/div/div/div[1]/a/div/p/text()').get().strip())[0]
        except IndexError:
            print('[-][-][-][-][-][-] IndexError')
            print(response.xpath('/html/body/div[5]/div/div/div/div[1]/a/div/p/text()').get().strip())
            item['episode'] = response.xpath('/html/body/div[5]/div/div/div/div[1]/a/div/p/text()').get().strip()
        yield scrapy.Request(webtoon, callback=self.webtoonCollect, meta={'webtoon':item})

    def webtoonCollect(self, response):
        item = response.meta.get('webtoon')
        DownloadUrl = response.xpath('/html/body/section/article/div/div/div/div[1]/img').xpath('@src').getall()[0]   #배너 수에 따라 xpath 달라질 수 있음 
        #item['file_urls'] = [DownloadUrl] #download 할때는 list로 들어가야함
        item['file_urls'] = DownloadUrl #DB로 저장할때는 원본 그대로
        item['extension'] = DownloadUrl.split('.')[-1]
        yield item
        
        
