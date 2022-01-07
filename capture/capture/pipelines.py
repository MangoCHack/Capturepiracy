# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from itemadapter import ItemAdapter
from io import BytesIO
import os
import csv


class CapturePipeline:
    def process_item(self, item, spider):
        return item


class WebtoonPipeline(FilesPipeline):
    '''
    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        for file_url in adapter['file_urls']:
            yield scrapy.Request(file_url)
    '''
    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = item['webtoonName']+'\\'+item['episode']+'\\'+item['hosturl']+'.'+item['extension']
        if not os.path.exists('E:\\CrawlCopyright\\Capturepiracy\\WebtoonImages\\'+item['webtoonName']+'\\'+item['episode']):
            os.makedirs('E:\\CrawlCopyright\\Capturepiracy\\WebtoonImages\\'+item['webtoonName']+'\\'+item['episode'])
        return file_name
    '''
    def get_images(self, response, request, info, *, item=None):
        path = self.file_path(request, response=response, info=info, item=item)
        orig_image = self._Image.open(BytesIO(response.body))
        image, buf = orig_image.save(BytesIO(),item['extension'])
        yield path, image, buf
    '''

class CsvPipeline(object):
    # 초기화 method
    # init method도 class가 초기화될 때 최초로 실행되므로 open_spider와 동일하게 사용가능
    def __init__(self):
        # 엑셀 처리 선언
        if not os.path.exists('..\\..\\CrawlDB\\'):
            os.makedirs('..\\..\\CrawlDB\\')
        self.file_opener = open("..\\..\\CrawlDB\\\CrawlDB.csv", "a", newline='')
        self.csv_writer = csv.DictWriter(self.file_opener, fieldnames=['hosturl','webtoonName','crawltime','updatetime','episode','file_urls','extension'])
        self.csv_writer.writeheader()
        '''
            extension = scrapy.Field()
            hosturl = scrapy.Field()
            updatetime = scrapy.Field()
            crawltime = scrapy.Field()
            webtoonName = scrapy.Field()
            episode = scrapy.Field()
            image_urls = scrapy.Field()
            images = scrapy.Field()
            file_urls = scrapy.Field()
            files = scrapy.Field()
        '''
    # 최초 1회 실행
    def open_spider(self, spider):
        spider.logger.info("CSV DB Writer Pipelines Started.")

    # 데이터를 크롤링할때 매번실행
    def process_item(self, item, spider):
        # 현재 item은 spider에서 item을 활용해서 작성했으므로 dictionary로 되어있다.
        self.csv_writer.writerow(item)
        return item

    # 마지막 1회 실행
    def close_spider(self, spider):

        # CSV 파일 닫기
        self.file_opener.close()

        spider.logger.info("CSV DB Writer Pipelines Finished")