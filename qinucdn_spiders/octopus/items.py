# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiniuItem(scrapy.Item):
    site = scrapy.Field()
    service_type = scrapy.Field()
    type = scrapy.Field()
    value = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()
