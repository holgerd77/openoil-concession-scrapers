# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy_ooc.item_loaders import ConcessionLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request

from scrapy_ooc.items import InDghDevItem


class InDghDevSpider(CrawlSpider):
    name = 'IN_DGH_DEV'
    allowed_domains = ['dghindia.org']
    start_urls = ['http://dghindia.org/PSC_D.aspx?tab=0']
    
    def parse_work_program_table(self, table_sel):
        table_list = [[u'Phase', u'2D(LKM)', u'3D(SKM)', u'Wells',],]
        tr_sel_list = table_sel.xpath('.//tr[not(@class="TableHead")]')
        for tr_sel in tr_sel_list:
            row_list = []
            row_list.append(tr_sel.xpath('(./td)[1]//text()').extract()[0])
            row_list.append(tr_sel.xpath('(./td)[2]//text()').extract()[0])
            row_list.append(tr_sel.xpath('(./td)[3]//text()').extract()[0])
            row_list.append(tr_sel.xpath('(./td)[4]//text()').extract()[0])
            table_list.append(row_list)
            
        return json.dumps(table_list)
    
    
    def parse_work_done_table(self, table_sel):
        table_list = [[u'Year', u'2D(LKM)', u'3D(SKM)', u'Wells',],]
        tr_sel_list = table_sel.xpath('.//tr[not(@class="TableHead") and not(@align="right")]')
        for tr_sel in tr_sel_list:
            row_list = []
            row_list.append(tr_sel.xpath('(./td)[1]//text()').extract()[0])
            row_list.append(tr_sel.xpath('(./td)[2]//text()').extract()[0])
            row_list.append(tr_sel.xpath('(./td)[3]//text()').extract()[0])
            row_list.append(tr_sel.xpath('(./td)[4]//text()').extract()[0])
            table_list.append(row_list)
            
        return json.dumps(table_list)
    
    
    def parse_discovery_table(self, table_sel):
        table_list = [[u'Discovery', u'Well',],]
        tr_sel_list = table_sel.xpath('.//tr[not(@class="TableHead")]')
        for tr_sel in tr_sel_list:
            row_list = []
            row_list.append(tr_sel.xpath('(./td)[1]/text()').extract()[0])
            row_list.append(tr_sel.xpath('(./td)[2]/text()').extract()[0])
            table_list.append(row_list)
            
        return json.dumps(table_list)
    
    
    def parse_detail_page(self, response):
        l = response.meta['l']
        
        xpath_base = '//table[@id="ctl00_ContentDGH_detailsVwGenInfo" or @id="ctl00_ContentDGH_detailsvwFields"]//'
        status_fields = [
            ('current_activity_status', 'Current Activity Status'),
            ('area_sq_km', 'Area(sq. km)'),
            ('date_of_signing_contract', 'Date of Signing Contract'),
            ('effective_date', 'Effective Date'),
            ('current_consortium', 'Current Consortium'),
            ('reservoir', 'Reservoir'),
            ('trap', 'Trap'),
            ('drive', 'Drive'),
            ('source', 'Source'),
            ('cap_seal', 'Cap/Seal'),
            #('', ''),
        ]
        
        for sf in status_fields:
            xpath = xpath_base + 'tr[contains(td, "' + sf[1] + '")]/td[2]/text()'
            l.add_value(sf[0], response.xpath(xpath).extract())
        
        #minimum_work_program_table = u''
        #xpath = '//table[@id="ctl00_ContentDGH_grdVwBlockMWP"]'
        #sel_list = response.xpath(xpath)
        #if len(sel_list) > 0:
        #    minimum_work_program_table = self.parse_work_program_table(sel_list[0])
        #l.add_value('minimum_work_program_table', minimum_work_program_table)
        
        yield l.load_item()
    
    
    def parse(self, response):
        tr_sel_list = response.xpath('//table[@id="ctl00_ContentDGH_grdVwAllFields"]//tr[not(@class="TableHead")]')
            
        # Complete: "...urls:", Extract: "...urls[0:3]:"
        for tr_sel in tr_sel_list[0:3]:
            url = 'http://dghindia.org/' + tr_sel.xpath('./td/a/@href').re('"", "([^"]*)')[0]
            l = ConcessionLoader(item=InDghDevItem(), selector=tr_sel, response=response)
            l.add_value('url', url)
            l.add_xpath('field_name', '(./td)[1]/a/text()')
            l.add_xpath('round', '(./td)[2]/text()')
            l.add_xpath('basin', '(./td)[3]/text()')
            yield Request(url, callback=self.parse_detail_page, meta={'l': l})
        
        