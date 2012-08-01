from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import log

from twisted.enterprise import adbapi
from techCrunch.processors import PostTimeEst


class TechCrunchHPPipeline(object):
    '''
        Passing scrapy container items into a MySQL database.
        Assume the db is already created.
    '''
    def __init__(self):
        log.msg('Pipes Ready!', level=log.INFO)
        self.postTimeEst = PostTimeEst()
        self.isql = "INSERT INTO homePage(headLine, headLineLink, postsBy, postsByLink, postTime, dlTimestamp, relTime) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        dispatcher.connect(self.spider_opened, signals.spider_opened)

    # make db connection as soon as spider is open
    def spider_opened(self, spider):
        log.msg('Connceting to MySQL', level=log.INFO)
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            db="TechCrunch",
            user='user_name',
            passwd='password',
            charset='utf8'
            )

    def spider_closed(self, spider):
        pass

    def process_item(self, item, spider):
        input = self.dbpool.runInteraction(self.MySQL_Query, item)
        input.addErrback(self.handle_error, item)

    def MySQL_Query(self, tx, item):
        # log.msg('query', level=log.INFO)
        relTime = [self.postTimeEst(item['postTime'][i], item['dlTimestamp'][0]) for i in range(len(item['postsBy']))]
        for i in range(len(item['postsBy'])):
            tx.execute(self.isql, (item['headLine'][i], item['headLineLink'][i], item['postsBy'][i], item['postsByLink'][i], item['postTime'][i], item['dlTimestamp'][0], relTime[i]))

    def handle_error(self, e, item):
        log.err("Error: %s %s" % (e, item['dlTimestamp']))
