import scrapy
import datetime
from capture.items import WebtoonItem
import re

class ToonSpider(scrapy.Spider):
    name = 'toon'
    #allowed_domains = ['toon123.com']
    start_urls = ['http://toon123.com/']

    def parse(self, response):
        webtoon_page='http://toon123.com'
        yield scrapy.Request(webtoon_page, callback=self.webtoonList)
         
    def webtoonList(self, response): #weekly webtoonList
        #webtoon_list = response.xpath('/html/body/div[7]/div/div[1]/div/div').xpath('//p/a').xpath('@href').getall()
        webtoon_list = response.css('.content-list').xpath('./ul/li/a').getall()
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
        
        webtoon = response.urljoin(response.css('.table').xpath('./tbody/tr/td/a/@href').get())
        item['hosturl'] = response.url.split('/')[2]
        item['webtoonName'] = response.css('.title').xpath('./text()').get()
        item['updatetime'] = response.css('.free-date').xpath('./text()').get().strip()
        now = datetime.datetime.now()
        item['crawltime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            item['episode'] = re.findall(r'([0-9]+)[권회화\.]',response.css('.episode-title').xpath('./text()').get().strip())[0]
        except IndexError:
            print('[-][-][-][-][-][-] IndexError')
            print(response.css('.episode-title').xpath('./text()').get().strip())
            item['episode'] = response.css('.episode-title').xpath('./text()').get().strip()
        yield scrapy.Request(webtoon, callback=self.webtoonCollect, meta={'webtoon':item})

    def webtoonCollect(self, response):
        item = response.meta.get('webtoon')
        
        DownloadUrl = re.search(r"var img_list = \[(.*)\];",str(response.body)).group(1).split(',')[0].strip('"')
        #item['file_urls'] = [DownloadUrl] #download 할때는 list로 들어가야함
        item['file_urls'] = DownloadUrl #DB로 저장할때는 원본 그대로
        item['extension'] = DownloadUrl.split('.')[-1]
        yield item