# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader.processor import Join


class UkDeccItem(scrapy.Item):
    url       = scrapy.Field()
    holder    = scrapy.Field()
    block     = scrapy.Field()
    subarea   = scrapy.Field()
    interest  = scrapy.Field()
    operator  = scrapy.Field()
    licence   = scrapy.Field() 

class TnEtapCItem(scrapy.Item):
    url           = scrapy.Field()
    concession    = scrapy.Field()
    partenaire    = scrapy.Field(output_processor=Join(separator=u'|'))
    participation = scrapy.Field(output_processor=Join(separator=u'|'))
    permis        = scrapy.Field()
    situation     = scrapy.Field()
    operateur     = scrapy.Field()
    date_de_decouverte = scrapy.Field()
    la_mise_en_production = scrapy.Field()
    formation     = scrapy.Field()
    puits_de_production = scrapy.Field()
    reserves_recuperables = scrapy.Field()
    production_journaliere_moyenne_2013 = scrapy.Field()

class InDghExpItem(scrapy.Item):
    url           = scrapy.Field()
    relinquished  = scrapy.Field()
    block_name    = scrapy.Field()
    round         = scrapy.Field()
    operator      = scrapy.Field()
    consortium    = scrapy.Field()
    status        = scrapy.Field()
    basin         = scrapy.Field()
    state         = scrapy.Field()
    date_of_signing = scrapy.Field()
    effective_date  = scrapy.Field()
    initial_area    = scrapy.Field()
    present_area    = scrapy.Field()
    relinquished_area = scrapy.Field()
    minimum_work_program_table = scrapy.Field()
    work_done_table = scrapy.Field()
    discovery_table = scrapy.Field()

class InDghDevItem(scrapy.Item):
    url           = scrapy.Field()
    field_name    = scrapy.Field()
    field_brief   = scrapy.Field()
    round         = scrapy.Field()
    basin         = scrapy.Field()
    current_activity_status = scrapy.Field()
    area_sq_km    = scrapy.Field()
    date_of_signing_contract = scrapy.Field()
    effective_date = scrapy.Field()
    current_consortium = scrapy.Field()
    reservoir      = scrapy.Field()
    trap           = scrapy.Field()
    drive          = scrapy.Field()
    source         = scrapy.Field()
    cap_seal       = scrapy.Field()
    gg_development_activities_table = scrapy.Field()
    yearly_production_table = scrapy.Field()
    development_wells_table = scrapy.Field()
    
class InDghWellsItem(scrapy.Item):
    url           = scrapy.Field()
    well_name     = scrapy.Field()
    block         = scrapy.Field()
    field         = scrapy.Field()
    basin         = scrapy.Field()
    round         = scrapy.Field()
    operator      = scrapy.Field()
    consortium    = scrapy.Field()
    state_name_offshore = scrapy.Field()
    latitude      = scrapy.Field()
    longitude     = scrapy.Field()
    
    