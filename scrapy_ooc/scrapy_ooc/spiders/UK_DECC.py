# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy_ooc.item_loaders import ConcessionLoader
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy_ooc.items import Concession


class UkDeccSpider(CrawlSpider):
    name = 'UK_DECC'
    allowed_domains = ['www.og.decc.gov.uk']
    start_urls = ['https://www.og.decc.gov.uk/eng/fox/decc/PED301X/companyBlocksNav']

    rules = (
        Rule(LinkExtractor(allow=r'COMPANY_GROUP_ID=893'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        l = ConcessionLoader(item=Concession(), response=response)
        l.add_value('url', response.url)
        l.add_xpath('holder', '//table[@class="setoutList"]//tr[2]/td[1]/text()')
        l.add_xpath('block', '//table[@class="setoutList"]//tr[2]/td[2]/text()', re='([^/]+)')
        l.add_xpath('subarea', '//table[@class="setoutList"]//tr[2]/td[2]/text()', re='/([^/]+)')
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return l.load_item()
