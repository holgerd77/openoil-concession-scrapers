# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy_ooc.item_loaders import ConcessionLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request

from scrapy_ooc.items import TnEtapCItem


class TnEtapCSpider(CrawlSpider):
    name = 'TN_ETAP_C'
    allowed_domains = ['www.etap.com.tn']
    start_urls = ['http://www.etap.com.tn/index.php?id=1160']

    rules = (
        # all sets: "fiche=", result limitation: "fiche=4" 
        #Rule(LinkExtractor(allow=r'fiche=4'), callback='parse_item', follow=False),
    )

    def parse_detail_page(self, response):
        l = response.meta['l']
        xpath = '//td[@class="bg_tab_concession"]/h4/strong/text()'
        l.add_value('concession', response.xpath(xpath).extract())
        l.add_value('url', response.url)
        xpath = '//table[@class="tab_concess"]//tr[contains(td/p/text(), "Permis")]/td[2]/text()'
        l.add_value('permis', response.xpath(xpath).extract())
        xpath = '//table[@class="tab_concess"]//tr[contains(td/p/text(), "Situation")]/td[2]/p/text()'
        l.add_value('situation', response.xpath(xpath).extract())
        xpath = '//table[@class="tab_concess"]//tr[contains(td/p/text(), "rateur")]/td[2]/p/text()'
        l.add_value('operateur', response.xpath(xpath).extract())
        xpath = '//table[@class="tab_concess"]//tr[contains(td/p/text(), "couverte")]/td[3]/p/text()'
        l.add_value('date_de_decouverte', response.xpath(xpath).extract())
        xpath = '//table[@class="tab_concess"]//tr[contains(td/p/text(), "La mise en production")]/td[3]/p/text()'
        l.add_value('la_mise_en_production', response.xpath(xpath).extract())
        xpath = '//table[@class="tab_concess"]//tr[contains(td/p/text(), "Formation")]/td[3]/p/text()'
        l.add_value('formation', response.xpath(xpath).extract())
        xpath = '//table[@class="tab_concess"]//tr[contains(td/p/text(), "Puits de production")]/td[3]/p/text()'
        l.add_value('puits_de_production', response.xpath(xpath).extract())
        xpath = '//table[@class="tab_concess"]//tr[contains(td/p/text(), "rables")]/td[2]/text()'
        l.add_value('reserves_recuperables', response.xpath(xpath).extract())
        xpath = '//table[@class="tab_concess"]//tr[contains(td/p/text(), "Moyenne")]/td[3]/p/text()'
        l.add_value('production_journaliere_moyenne_2013', response.xpath(xpath).extract())
        
        yield l.load_item()
    
    
    def parse(self, response):
        tables = response.xpath('//td[@class="cartouche_contenu"]/div/div/table')
        
        # Complete: "...tables:", Extract: "...tables[0:3]:"
        for table in tables:
            url  = 'http://www.etap.com.tn'
            url += table.xpath('.//a/@href').extract()[0]
            l = ConcessionLoader(item=TnEtapCItem(), response=response)
            l.add_value('partenaire', table.xpath('.//table[@class="tab_concess"]//tr[not(@class="title")]/td[1]/p/text()').extract())
            l.add_value('participation', table.xpath('.//table[@class="tab_concess"]//tr[not(@class="title")]/td[2]/p/text()').extract())
            yield Request(url, callback=self.parse_detail_page, meta={'l': l})
        
