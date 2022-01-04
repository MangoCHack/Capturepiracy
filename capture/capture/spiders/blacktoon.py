import scrapy
import datetime
from capture.items import WebtoonItem
import re
from scrapy_selenium import SeleniumRequest

class BlacktoonSpider(scrapy.Spider): #캡챠 있음
    name = 'blacktoon'
    #allowed_domains = ['blacktoon132.com']
    start_urls = ['https://blacktoon140.com/']

    def parse(self, response):

        webtoon_page='https://blacktoon140.com/'
        
        yield SeleniumRequest(url=webtoon_page, callback=self.webtoonList)
         
    def webtoonList(self, response): #weekly webtoonList, 다음페이지 이동 코드 업데이트 필요
        #webtoon_list = response.xpath('/html/body/div[7]/div/div[1]/div/div').xpath('//p/a').xpath('@href').getall()
        scrapy.view(response)
        webtoon_list = response.css('.card-fluid').getall()
        print(webtoon_list[0])
        print(webtoon_list[-1])
        print(len(webtoon_list))
        '''
        today = []
        for i in range(len(webtoon_list)):
            flag = re.findall(r'하루전',webtoon_list[i])
            url = re.findall(r'a href="(/(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"',webtoon_list[i])
            if len(flag) == 0:
                continue
            else:
                today.append(response.urljoin(url[0]))
        print(today)
        for n, webtoon in enumerate(today):
            yield scrapy.Request(webtoon, callback=self.webtoonPage)
        
    def webtoonPage(self, response): #웹툰 몇화 고르는 페이지 접근해서 데이터 추출
        item = WebtoonItem()
        
        webtoon = response.urljoin(response.css('.list').xpath('./li/a').xpath('@href').get())
        item['hosturl'] = response.url.split('/')[2]
        item['webtoonName'] = response.css('.text-box').xpath('./h1/text()').get()
        item['updatetime'] = response.css('.date').xpath('./text()').get()
        now = datetime.datetime.now()
        item['crawltime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            item['episode'] = re.findall(r'([0-9]+)[권회화\.]',response.css('.subject').xpath('./text()').get())[0]
        except IndexError:
            print('[-][-][-][-][-][-] IndexError')
            print(response.css('.subject').xpath('./text()').get())
            item['episode'] = response.css('.subject').xpath('./text()').get()
        yield scrapy.Request(webtoon, callback=self.webtoonCollect, meta={'webtoon':item})

    def webtoonCollect(self, response):
        item = response.meta.get('webtoon')
        
        DownloadUrl = response.css('.wbody').xpath('./img').xpath('@src').get()   #배너 수에 따라 xpath 달라질 수 있음 
        #item['file_urls'] = [DownloadUrl] #download 할때는 list로 들어가야함
        item['file_urls'] = DownloadUrl #DB로 저장할때는 원본 그대로
        item['extension'] = DownloadUrl.split('.')[-1]
        yield item
    '''