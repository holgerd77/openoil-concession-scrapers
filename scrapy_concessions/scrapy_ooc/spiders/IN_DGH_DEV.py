# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import log
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy_ooc.item_loaders import ConcessionLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request

from scrapy_ooc.items import InDghDevItem


class InDghDevSpider(CrawlSpider):
    name = 'IN_DGH_DEV'
    allowed_domains = ['dghindia.org']
    start_urls = ['http://dghindia.org/PSC_D.aspx?tab=0']
    
    def parse_dev_activities_table(self, table_sel):
        table_list = [[u'Year', u'2D(LKM)', u'3D(SKM)', u'Wells',],]
        tr_sel_list = table_sel.xpath('.//tr[not(@class="TableHead")]')
        for tr_sel in tr_sel_list:
            row_list = []
            row_list.append(tr_sel.xpath('(./td)[1]//text()').extract()[0])
            row_list.append(tr_sel.xpath('(./td)[2]//text()').extract()[0])
            row_list.append(tr_sel.xpath('(./td)[3]//text()').extract()[0])
            row_list.append(tr_sel.xpath('(./td)[4]//text()').extract()[0])
            table_list.append(row_list)
            
        return json.dumps(table_list)
    
    
    def parse_yearly_production_table(self, table_sel):
        table_list = [[u'Year', u'Oil(\'000T)', u'Gas(mm3)'],]
        tr_sel_list = table_sel.xpath('.//tr[not(@class="TableHead")]')
        cnt = 0
        for tr_sel in tr_sel_list:
            row_list = []
            cnt += 1
            if cnt == len(tr_sel_list):
                row_list.append(u'Total')
            else:
                row_list.append(tr_sel.xpath('(./td)[1]/a/text()').extract()[0])
            row_list.append(tr_sel.xpath('(./td)[2]//text()').extract()[0])
            row_list.append(tr_sel.xpath('(./td)[3]//text()').extract()[0])
            table_list.append(row_list)
            
        return json.dumps(table_list)
    
    
    def parse_dev_wells_table(self, table_sel):
        table_list = [[u'Well', u'Url', u'Status',],]
        tr_sel_list = table_sel.xpath('.//tr[not(@class="TableHead")]')
        for tr_sel in tr_sel_list:
            row_list = []
            row_list.append(tr_sel.xpath('(./td)[1]/a/text()').extract()[0])
            url = u'http://dghindia.org/' + tr_sel.xpath('(./td)[1]/a/@href').re('"", "([^"]*)')[0]
            row_list.append(url)
            self.log("Writing well url to file %s." % self.well_urls_file.name, level=log.INFO)
            self.well_urls_file.write(url + '\n')
            row_list.append(tr_sel.xpath('(./td)[2]//text()').extract()[0])
            table_list.append(row_list)
            
        return json.dumps(table_list)
    
    
    def parse_detail_page(self, response):
        l = response.meta['l']
        
        xpath = '//span[@id="ctl00_ContentDGH_lblFieldBrief"]/text()'
        l.add_value('field_brief', response.xpath(xpath).extract())
        
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
        
        gg_development_activities_table = u''
        xpath = '//table[@id="ctl00_ContentDGH_grdViewGandGDevelopmentActivity"]'
        sel_list = response.xpath(xpath)
        if len(sel_list) > 0:
            gg_development_activities_table = self.parse_dev_activities_table(sel_list[0])
        l.add_value('gg_development_activities_table', gg_development_activities_table)
        
        yearly_production_table = u''
        xpath = '//table[@id="ctl00_ContentDGH_grdViewYearlyProduction"]'
        sel_list = response.xpath(xpath)
        if len(sel_list) > 0:
            yearly_production_table = self.parse_yearly_production_table(sel_list[0])
        l.add_value('yearly_production_table', yearly_production_table)
        
        development_wells_table = u''
        xpath = '//table[@id="ctl00_ContentDGH_grdVwDevelopmentWells"]'
        sel_list = response.xpath(xpath)
        if len(sel_list) > 0:
            development_wells_table = self.parse_dev_wells_table(sel_list[0])
        l.add_value('development_wells_table', development_wells_table)
        
        yield l.load_item()
    
    
    def parse(self, response):
        self.well_urls_file = open('IN_DGH_DEV_well_urls.txt', 'w')
        tr_sel_list = response.xpath('//table[@id="ctl00_ContentDGH_grdVwAllFields"]//tr[not(@class="TableHead")]')
            
        # Complete: "...urls:", Extract: "...urls[0:3]:"
        for tr_sel in tr_sel_list:
            url = 'http://dghindia.org/' + tr_sel.xpath('./td/a/@href').re('"", "([^"]*)')[0]
            l = ConcessionLoader(item=InDghDevItem(), selector=tr_sel, response=response)
            l.add_value('url', url)
            l.add_xpath('field_name', '(./td)[1]/a/text()')
            l.add_xpath('round', '(./td)[2]/text()')
            l.add_xpath('basin', '(./td)[3]/text()')
            yield Request(url, callback=self.parse_detail_page, meta={'l': l})
    
        
        