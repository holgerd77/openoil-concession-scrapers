# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy_ooc.item_loaders import ContractLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request

from scrapy_ooc.items import PePerupetroItem


class PePerupetroSpider(CrawlSpider):
    name = 'PE_PERUPETRO'
    allowed_domains = ['www.perupetro.com.pe']
    start_urls = ['http://www.perupetro.com.pe/relaciondecontratos/relacion.jsp?token=99']


    def parse_detail_page(self, response):
        lote = response.meta['lote']

        table_rows = response.xpath('//table[@class="tablita"]//tr[position() > 1]')
        for row in table_rows:
            l = ContractLoader(item=PePerupetroItem(), response=response)
            l.add_value('url', response.url)
            l.add_value('lote', lote)
            if len(table_rows) == 1:
                l.add_value('no_de_modification', row.xpath('./td[2]//text()').extract())
                l.add_value('fecha_de_suscription', row.xpath('./td[3]//text()').extract())
                l.add_value('testimonios_y_modificationes', row.xpath('./td[4]//text()').extract())
                l.add_value('no_de_decreto_supremo', row.xpath('./td[5]//text()').extract())
                l.add_value('notaria', row.xpath('./td[6]//text()').extract())
                l.add_value('pdf_url', row.xpath('./td[4]//a/@href').extract())
            else:
                l.add_value('no_de_modification', row.xpath('./td[not(@rowspan)][1]//text()').extract())
                l.add_value('fecha_de_suscription', row.xpath('./td[not(@rowspan)][2]//text()').extract())
                l.add_value('testimonios_y_modificationes', row.xpath('./td[not(@rowspan)][3]//text()').extract())
                l.add_value('no_de_decreto_supremo', row.xpath('./td[not(@rowspan)][4]//text()').extract())
                l.add_value('notaria', row.xpath('./td[not(@rowspan)][5]//text()').extract())
                l.add_value('pdf_url', row.xpath('./td[not(@rowspan)][3]//a/@href').extract())
            yield l.load_item()
    
    
    def parse(self, response):
        url_tokens = response.xpath('//select[@name="id_lote"]/option')
        
        # Complete: "...url_tokens:", Extract: "...url_tokens[0:3]:"
        for token in url_tokens:
            url  = 'http://www.perupetro.com.pe/relaciondecontratos/relacion.jsp?token=' + token.xpath('./@value').extract()[0]
            lote = (token.xpath('./text()').extract()[0]).strip()
            yield Request(url, callback=self.parse_detail_page, meta={'lote': lote})
        
