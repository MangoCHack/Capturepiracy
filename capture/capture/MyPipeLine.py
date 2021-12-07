import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from io import BytesIO
import os


class WebtoonPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        return item
        
    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = item['webtoonName']+'\\'+item['episode']+'\\'+item['hosturl']+'.'+item['extension']
        if not os.path.exists('E:\\CrawlCopyright\\Capturepiracy\\WebtoonImages\\'+item['webtoonName']+'\\'+item['episode']):
            os.makedirs('E:\\CrawlCopyright\\Capturepiracy\\WebtoonImages\\'+item['webtoonName']+'\\'+item['episode'])
        print(file_name)
        return file_name

    def get_images(self, response, request, info, *, item=None):
        path = self.file_path(request, response=response, info=info, item=item)
        orig_image = self._Image.open(BytesIO(response.body))
        image, buf = orig_image.save(BytesIO(),item['extension'])
        yield path, image, buf

    