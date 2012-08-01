from scrapy.item import Item, Field


class TechCrunchItem(Item):
    postsBy = Field()
    postsByLink = Field()
    postTime = Field()
    headLine = Field()
    headLineLink = Field()
    dlTimestamp = Field()
