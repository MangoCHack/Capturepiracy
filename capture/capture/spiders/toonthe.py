import scrapy
import datetime
from capture.items import WebtoonItem
import re
import base64

class ToontheSpider(scrapy.Spider):
    name = 'toonthe'
    #allowed_domains = ['v4.toonthe.com']
    start_urls = ['https://v33.toonthe.com/']

    def parse(self, response):

        webtoon_page='https://v33.toonthe.com/?sort=%EC%B5%9C%EC%8B%A0'
        yield scrapy.Request(webtoon_page, callback=self.webtoonList)
         
    def webtoonList(self, response): #weekly webtoonList
        #webtoon_list = response.xpath('/html/body/div[7]/div/div[1]/div/div').xpath('//p/a').xpath('@href').getall()
        
        webtoon_list = response.css('.section-item-inner').getall()
        today = []
        for i in range(len(webtoon_list)):
            flag = re.findall(r'>업데이트<',webtoon_list[i])
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
        
        webtoon = response.urljoin(response.css('.content__title').xpath('./@data-role').get())
        item['hosturl'] = response.url.split('/')[2]
        item['webtoonName'] = response.css('.bt_title').xpath('./text()').get()
        item['updatetime'] = response.css('.episode__index').xpath('./text()').get()
        now = datetime.datetime.now()
        item['crawltime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            item['episode'] = re.findall(r'([0-9]+)[권회화\.]',response.css('.content__title').xpath('./text()').get().strip())[0]
        except Exception as e:
            print(e)
            print(response.css('.content__title').xpath('./text()').get().strip())
            item['episode'] = response.css('.content__title').xpath('./text()').get().strip()
        yield scrapy.Request(webtoon, callback=self.webtoonCollect, meta={'webtoon':item})

    def webtoonCollect(self, response):
        item = response.meta.get('webtoon')
        SourceEncode = re.search(r'var toon_img = "(.*)";',str(response.body)).group(1)
        SourceDecode = base64.b64decode(SourceEncode)
        DownloadUrl = re.findall(r'src="(.*?)"',str(SourceDecode))[0]
        #item['file_urls'] = [DownloadUrl] #download 할때는 list로 들어가야함
        item['file_urls'] = DownloadUrl #DB로 저장할때는 원본 그대로
        item['extension'] = DownloadUrl.split('.')[-1]
        yield item