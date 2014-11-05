# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy_ooc.item_loaders import ConcessionLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request

from scrapy_ooc.items import ThPttepItem


class ThPttepSpider(CrawlSpider):
    '''
    Scraping main page can take several attempts due to slow connection
    DEV comment: scraper can be tested by changing "start_urls" to detail page, "def parse_item" -> "def parse"
    and commenting out "Rule" (so that data is scraped directly from detail page)
    '''
    name = 'TH_PTTEP'
    allowed_domains = ['www.pttep.com']
    #start_urls = ['http://www.pttep.com/en/ourBusiness_EAndPprojectsDetail.aspx?ContentID=4&type=1']
    start_urls = ['http://www.pttep.com/en/ourBusiness_EAndPprojects.aspx?type=1&Region=0&Phase=0&Investment=0&page=all']

    rules = (
        # all sets: "ContentID=", result limitation: "ContentID=7" 
        Rule(LinkExtractor(allow=r'ContentID='), callback='parse_item', follow=False),
    )
    
    def parse_partners_table(self, response):
        table_list = [[u'Concession Name', u'Percent Shares',],]
        tr_sel_list = response.xpath('//span[@id="ctl00_ContentPlaceHolder1_lblDetail"]/table//tr')[1:]
        for tr_sel in tr_sel_list:
            concession = tr_sel.xpath('(./td)[1]/text()').extract()[0]
            partners = tr_sel.xpath('(./td)[2]//text()').extract()
            for p in partners:
                if u"%" in p:
                    row_list = []
                    row_list.append(concession)
                    row_list.append(p)
                    table_list.append(row_list)
            
        return json.dumps(table_list)
    
    
    #def parse(self, response):
    def parse_item(self, response):
        l = ConcessionLoader(item=ThPttepItem(), response=response)
        l.add_value('url', response.url)
        l.add_xpath('project', '//span[@id="ctl00_ContentPlaceHolder1_lblSubject"]/text()', re='(.*) Project')
        
        xpath_base = '//table[@class="borderT"]//'
        fields = [
            ('type_of_business', 'Type of Business'),
            ('concessions', 'Concessions'),
            ('area', 'Area'),
            ('location', 'Location'),
            ('operator', 'Operator'),
            ('phase', 'Phase'),
            ('investment_type', 'Investment Type'),
            ('petroleum_fields', 'Petroleum Fields'),
            ('type_of_petroleum', 'Type of Petroleum'),
            ('signing_date', 'Signing Date'),
            ('production_start_up', 'Production Start-up'),
            ('website', 'Website'),
            #('', ''),
        ]
        
        for f in fields:
            xpath = xpath_base + 'tr[contains(td/strong, "' + f[1] + '")]/td[2]/span/text()'
            l.add_value(f[0], response.xpath(xpath).extract())
        
        xpath = xpath_base + 'tr[contains(td/strong, "Partners")]/td[2]//table//tr[1]/td[1]/text()'
        partners_str = response.xpath(xpath).extract()[0]
        
        if partners_str == u"Please see below table":
            l.add_value('partners', self.parse_partners_table(response))
        else:
            tr_sel_list = response.xpath('//td[@id="ctl00_ContentPlaceHolder1_tdPortion"]/table//tr')
            table_list = [[u'Concession Name', u'Percent Shares',],]
            for tr_sel in tr_sel_list:
                partner = u" ".join(tr_sel.xpath('./td/text()').extract())
                table_list.append([u'PROJECT', partner],)
            l.add_value('partners', json.dumps(table_list))
        
        yield l.load_item()
        