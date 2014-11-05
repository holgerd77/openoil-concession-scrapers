# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader.processor import Join


class PePerupetroItem(scrapy.Item):
    url           = scrapy.Field()
    lote          = scrapy.Field()
    no_de_modification = scrapy.Field()
    fecha_de_suscription = scrapy.Field()
    testimonios_y_modificationes = scrapy.Field()
    no_de_decreto_supremo = scrapy.Field()
    notaria       = scrapy.Field()
    pdf_url       = scrapy.Field()

