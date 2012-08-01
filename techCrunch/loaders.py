from scrapy.contrib.loader.processor import MapCompose, Identity
from scrapy.contrib.loader import XPathItemLoader
from scrapy import log

from techCrunch.items import TechCrunchItem


class RootItemLoader(XPathItemLoader):
    log.msg("loading loaders", level=log.INFO)
    default_input_processor = Identity()
    default_ouput_processor = Identity()


class TCLoader(RootItemLoader):
    default_item_class = TechCrunchItem
    headLine_in = MapCompose(unicode.strip)
