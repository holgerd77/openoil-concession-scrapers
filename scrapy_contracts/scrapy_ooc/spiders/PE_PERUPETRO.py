# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy_ooc.item_loaders import ContractLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request

from scrapy_ooc.items import PePerupetroItem


class PePerupetroSpider(CrawlSpider):
    name = 'PE_PERUPETRO'
    allowed_domains = ['www.etap.com.tn']
    start_urls = ['http://www.etap.com.tn/index.php?id=1160']

    def parse_detail_page(self, response):
        l = response.meta['l']
        xpath = '//td[@class="bg_tab_concession"]/h4/strong/text()'
        l.add_value('concession', response.xpath(xpath).extract())
        l.add_value('url', response.url)
        xpath = '//table[@class="tab_concess"]//tr[contains(td/p/text(), "Permis")]/td[2]/text()'
        l.add_value('permis', response.xpath(xpath).extract())
        
        yield l.load_item()
    
    
    def parse(self, response):
        tables = response.xpath('//td[@class="cartouche_contenu"]/div/div/table')
        
        # Complete: "...tables:", Extract: "...tables[0:3]:"
        for table in tables[0:3]:
            url  = 'http://www.etap.com.tn'
            url += table.xpath('.//a/@href').extract()[0]
            l = ContractLoader(item=PePerupetroItem(), response=response)
            l.add_value('partenaire', table.xpath('.//table[@class="tab_concess"]//tr[not(@class="title")]/td[1]/p/text()').extract())
            yield Request(url, callback=self.parse_detail_page, meta={'l': l})
        
