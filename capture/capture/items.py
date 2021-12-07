# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CaptureItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ImageItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class WebtoonItem(scrapy.Item):
    # define the fields for your item here like:
    extension = scrapy.Field()
    hosturl = scrapy.Field()
    updatetime = scrapy.Field()
    crawltime = scrapy.Field()
    webtoonName = scrapy.Field()
    episode = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    