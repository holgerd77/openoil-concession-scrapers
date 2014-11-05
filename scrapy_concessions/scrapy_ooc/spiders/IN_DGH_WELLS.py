# -*- coding: utf-8 -*-
import json, os
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy_ooc.item_loaders import ConcessionLoader
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.http import Request

from scrapy_ooc.items import InDghWellsItem


class InDghWellsSpider(CrawlSpider):
    
    name = 'IN_DGH_WELLS'
    allowed_domains = ['dghindia.org']
    start_urls = ['http://dghindia.org/PSC_D.aspx?tab=2']
    
    def parse_detail_page(self, response):
        l = response.meta['l']
        xpath_base = '//table[@id="ctl00_ContentDGH_dtlsView"]//'
        
        status_fields = [
            ('well_name', 'Well Name'),
            ('block', 'Block'),
            ('field', 'Field'),
            ('basin', 'Basin'),
            ('round', 'Round'),
            ('operator', 'Operator'),
            ('consortium', 'consortium'),
            ('state_name_offshore', 'State Name/Offshore'),
        ]
        
        for sf in status_fields:
            xpath = xpath_base + 'tr[contains(td, "' + sf[1] + '")]/td[2]/text()'
            l.add_value(sf[0], response.xpath(xpath).extract())
        
        xpath = xpath_base + 'tr[contains(td, "Latitude")]/td[2]/span/text()'
        l.add_value('latitude', " ".join(map(lambda str: str.strip(), response.xpath(xpath).extract())))
        xpath = xpath_base + 'tr[contains(td, "Longitude")]/td[2]/span/text()'
        l.add_value('longitude', " ".join(map(lambda str: str.strip(), response.xpath(xpath).extract())))
        
        yield l.load_item()
    
    
    def parse(self, response):
        file_name = 'IN_DGH_DEV_well_urls.txt'
        
        if not os.path.isfile(file_name):
            msg  = "Scraper has to be run after IN_DGH_DEV scraper, "
            msg += "which creates a %s file containing well urls " % file_name
            msg += "(no file %s found in directory)." % file_name
            raise CloseSpider(msg)
        
        dev_url_list = []
        with open(file_name) as inputfile:
            for line in inputfile:
                dev_url_list.append(line.strip())
        
        disc_url_list = response.xpath('//table[@id="ctl00_ContentDGH_grdVwAllDiscoveries"]//tr[not(@class="TableHead")]/td[2]/a/@href').re('"", "([^"]*)')
        disc_url_list = map(lambda str: u'http://dghindia.org/' + str, disc_url_list)
        
        url_list = dev_url_list + disc_url_list
        
        # Complete: "...urls:", Extract: "...urls[0:3]:"
        for url in url_list:
            l = ConcessionLoader(item=InDghWellsItem(), response=response) 
            l.add_value('url', url)
            yield Request(url, callback=self.parse_detail_page, meta={'l': l})
        
        