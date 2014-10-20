# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Concession(scrapy.Item):
    url      = scrapy.Field()
    holder   = scrapy.Field()
    block    = scrapy.Field()
    subarea  = scrapy.Field()
    interest = scrapy.Field()
    operator = scrapy.Field() 
