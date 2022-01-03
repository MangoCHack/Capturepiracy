import scrapy
import datetime
from capture.items import WebtoonItem
import re

class WtwtSpider(scrapy.Spider):
    name = 'wtwt'
    #allowed_domains = ['wtwt106.com']
    start_urls = ['https://wtwt106.com/']

    def parse(self, response):

        webtoon_page='https://wtwt111.com/w1?type1=day&type2=recent&o=n'
        if str(response.body).find('\\xbb\\xf5\\xc1\\xd6\\xbc\\xd2 \\xc0\\xcc\\xb5\\xbf\\xc7\\xcf\\xb1\\xe2') > 0 :
            webtoon_page=response.css('.btnx').xpath('./@href').get()+'/w1?type1=day&type2=recent&o=n'
        yield scrapy.Request(webtoon_page, callback=self.webtoonList)
         
    def webtoonList(self, response): #weekly webtoonList, 다음페이지 이동 코드 업데이트 필요
        #webtoon_list = response.xpath('/html/body/div[7]/div/div[1]/div/div').xpath('//p/a').xpath('@href').getall()
        
        webtoon_list = response.css('.gallery').xpath('./li').getall()
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