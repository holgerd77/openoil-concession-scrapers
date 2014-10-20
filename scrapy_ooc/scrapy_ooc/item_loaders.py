from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst

class ConcessionLoader(ItemLoader):

    default_output_processor = TakeFirst()