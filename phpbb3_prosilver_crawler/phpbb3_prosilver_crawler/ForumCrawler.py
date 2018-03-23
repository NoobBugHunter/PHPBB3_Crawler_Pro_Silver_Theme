##############################################################################
#
# Crawler for PHPBB3 Pro Silver theme - 6 March 2018
#  Crawls each subforum, respective topics and posts
#
# Syntax: scrapy crawl
#
##############################################################################

import scrapy
from spiders.ForumSpider import ForumSpider
from spiders.TopicSpider import TopicSpider
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

configure_logging()
settings=get_project_settings()
runner = CrawlerRunner(settings)

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(ForumSpider)
    yield runner.crawl(TopicSpider)
    reactor.stop()

crawl()
reactor.run()
