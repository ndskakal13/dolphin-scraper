# -*- coding: utf-8 -*-

# Models for scraped items defined here.
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GeturlsItem(scrapy.Item):
    URL = scrapy.Field()
