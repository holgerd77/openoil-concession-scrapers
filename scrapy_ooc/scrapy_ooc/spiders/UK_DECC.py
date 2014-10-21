# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy_ooc.item_loaders import ConcessionLoader
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy_ooc.items import UkDeccItem


class UkDeccSpider(CrawlSpider):
    name = 'UK_DECC'
    allowed_domains = ['www.og.decc.gov.uk']
    start_urls = ['https://www.og.decc.gov.uk/eng/fox/decc/PED301X/companyBlocksNav']

    rules = (
        Rule(LinkExtractor(allow=r'COMPANY_GROUP_ID=325'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        rows = response.xpath('//table[@class="setoutList"]//tr[@style="border:0px;"]')
        holder = ''
        for row in rows:
            new_holder_list = row.xpath('td[1]/text()').extract()
            if len(new_holder_list) > 0:
                holder = new_holder_list[0]
            l = ConcessionLoader(item=UkDeccItem(), selector=row, response=response)
            l.add_value('url', response.url)
            l.add_value('holder', holder)
            l.add_xpath('block', 'td[2]/text()', re='([^/]+)')
            l.add_xpath('subarea', 'td[2]/text()', re='/([^/]+)')
            l.add_xpath('interest', 'td[3]/text()')
            l.add_xpath('operator', 'td[4]/text()')
            l.add_xpath('licence', 'td[5]/text()')
        
            yield l.load_item()
