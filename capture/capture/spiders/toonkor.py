import scrapy
import datetime
from capture.items import WebtoonItem
import feedparser
import re

class ToonkorSpider(scrapy.Spider):
    name = 'toonkor'
    #allowed_domains = ['tkor.toys']
    start_urls = ['https://tkor.house/%EB%AC%B4%EB%A3%8C%EC%9B%B9%ED%88%B0']

    def parse(self, response):
        
        rss_page='https://tkor.house/bbs/rss.php?bo_table=wtoon'
        NewFeed = feedparser.parse(rss_page)
        entries = NewFeed.entries
        for entry in entries:
            item = WebtoonItem()
            item['hosturl'] = response.url.split('/')[2]
            try:
                item['webtoonName'] = re.findall(r'(.+?) ([0-9]+)[화회]',entry.title)[0][0]
                item['episode'] = re.findall(r'([0-9]+)[화회]',entry.title)[0].strip()
            except Exception as e:
                item['webtoonName'] = entry.title
                item['episode'] = entry.title.split(' ')[-1]
            item['updatetime'] = entry.updated #업데이트 시간 정규화 시키기
            now = datetime.datetime.now()
            item['crawltime'] = now.strftime('%Y-%m-%d %H:%M:%S')
            item['file_urls'] = re.findall(r'src="(.*?)"',entry.summary)[0].strip()
            item['extension'] = item['file_urls'].split('.')[-1]
            yield item
        