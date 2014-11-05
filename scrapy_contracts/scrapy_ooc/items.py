# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader.processor import Join


class PePerupetroItem(scrapy.Item):
    url           = scrapy.Field()
    concession    = scrapy.Field()
    partenaire    = scrapy.Field(output_processor=Join(separator=u'|'))
    permis        = scrapy.Field()

