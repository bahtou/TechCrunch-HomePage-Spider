from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy import log

from techCrunch.loaders import TCLoader
from datetime import datetime
from pytz import timezone


class techCrunch(BaseSpider):
    name = 'tC'
    allowed_domains = ['techcrunch.com']

    # This gets your start page and directs it to get parse manager
    def start_requests(self):
        return [Request("http://techcrunch.com", callback=self.parseMgr)]

    # the parse manager deals out what to parse and start page extraction
    def parseMgr(self, response):
        log.msg("ParseManager", level=log.INFO)
        # Front page
        yield self.pageParser(response)

        # Tech crunch has many pages associated with the homepage.
        # Change pages to the number of pages to extract
        pages = 2
        for i in range(1, pages):
            yield Request('http://www.techcrunch.com/page/%s' % (i + 1), callback=self.parseMgr)

    def pageParser(self, response):
        log.msg("Response: %s" % response.url, level=log.INFO)

        loader = TCLoader(response=response)
        loader.add_value('dlTimestamp', datetime.now(timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S %z"))
        loader.add_xpath("postsBy", "//div[@class='publication-info']/div[@class='by-line']/a/text()")
        loader.add_xpath("postsByLink", "//div[@class='publication-info']/div[@class='by-line']/a/@href")
        loader.add_xpath("postTime", "//div[@class='publication-info']/div[@class='post-time']/text()")
        loader.add_xpath("headLine", "//div/h2[@class='headline']/a/@title")
        loader.add_xpath("headLineLink", "//div/h2[@class='headline']/a/@href")

        return loader.load_item()
