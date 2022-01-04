import scrapy
import datetime
from capture.items import WebtoonItem
import re
import base64

class SureSpider(scrapy.Spider):
    name = 'sure'
    #allowed_domains = ['sure-02.link']
    start_urls = ['https://sure-02.link/']

    def parse(self, response):
        
        webtoon_pages=['https://sure-02.link/%EC%9B%B9%ED%88%B0/%EC%9A%94%EC%9D%BC/%EC%9B%94?&sort=%EC%B5%9C%EC%8B%A0','https://sure-02.link/%EC%9B%B9%ED%88%B0/%EC%9A%94%EC%9D%BC/%ED%99%94?&sort=%EC%B5%9C%EC%8B%A0','https://sure-02.link/%EC%9B%B9%ED%88%B0/%EC%9A%94%EC%9D%BC/%EC%88%98?&sort=%EC%B5%9C%EC%8B%A0','https://sure-02.link/%EC%9B%B9%ED%88%B0/%EC%9A%94%EC%9D%BC/%EB%AA%A9?&sort=%EC%B5%9C%EC%8B%A0','https://sure-02.link/%EC%9B%B9%ED%88%B0/%EC%9A%94%EC%9D%BC/%EA%B8%88?&sort=%EC%B5%9C%EC%8B%A0','https://sure-02.link/%EC%9B%B9%ED%88%B0/%EC%9A%94%EC%9D%BC/%ED%86%A0?&sort=%EC%B5%9C%EC%8B%A0','https://sure-02.link/%EC%9B%B9%ED%88%B0/%EC%9A%94%EC%9D%BC/%EC%9D%BC?&sort=%EC%B5%9C%EC%8B%A0']
        for webtoon_page in webtoon_pages:
            yield scrapy.Request(webtoon_page, callback=self.webtoonList)
         
    def webtoonList(self, response): #weekly webtoonList, 다음페이지 이동 코드 업데이트 필요
        #webtoon_list = response.xpath('/html/body/div[7]/div/div[1]/div/div').xpath('//p/a').xpath('@href').getall()
        
        webtoon_list = response.css('.section-item-inner').getall()
        today = []
        for i in range(len(webtoon_list)):
            flag = re.findall(r'>오늘<',webtoon_list[i])
            url = re.findall(r'a href="(/(?:[a-zA-Z]|[0-9]|[$\-@\.&+:/?=]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"',webtoon_list[i])
            if len(flag) == 0:
                continue
            else:
                today.append(response.urljoin(url[0]))
        print(len(today))
        for n, webtoon in enumerate(today):
            yield scrapy.Request(webtoon, callback=self.webtoonPage)
        
    def webtoonPage(self, response): #웹툰 몇화 고르는 페이지 접근해서 데이터 추출
        item = WebtoonItem()
        
        webtoon = response.urljoin(response.css('.bt-table').xpath('./tbody/tr/td[2]/a/@href').get().strip())
        item['hosturl'] = response.url.split('/')[2]
        item['webtoonName'] = response.css('.bt_title').xpath('./text()').get().strip()
        item['updatetime'] = response.css('.td_date').xpath('./div/text()').get()
        now = datetime.datetime.now()
        item['crawltime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        try:
            item['episode'] = re.findall(r'([0-9]+)[권회화\.]',response.css('.bt-table').xpath('./tbody/tr/td[2]/a/text()').get().strip())[0]
        except IndexError:
            print('[-][-][-][-][-][-] IndexError')
            print(response.css('.bt-table').xpath('./tbody/tr/td[2]/a/text()').get().strip())
            item['episode'] = response.css('.bt-table').xpath('./tbody/tr/td[2]/a/text()').get().strip()
        yield scrapy.Request(webtoon, callback=self.webtoonCollect, meta={'webtoon':item})

    def webtoonCollect(self, response):
        item = response.meta.get('webtoon')
        #bo_v_con > img:nth-child(3)
        SourceEncode = re.search(r"var toon_img = \\'(.*)\\';",str(response.body)).group(1)
        SourceDecode = base64.b64decode(SourceEncode)
        DownloadUrl = re.findall(r'src="(.*?)"',str(SourceDecode))[0]
        #item['file_urls'] = [DownloadUrl] #download 할때는 list로 들어가야함
        item['file_urls'] = DownloadUrl #DB로 저장할때는 원본 그대로
        item['extension'] = DownloadUrl.split('.')[-1]
        yield item