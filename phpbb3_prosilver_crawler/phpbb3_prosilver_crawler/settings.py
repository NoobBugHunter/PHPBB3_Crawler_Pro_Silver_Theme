# -*- coding: utf-8 -*-

# Scrapy settings for phpbb3_prosilver_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'phpbb3_prosilver_crawler'

SPIDER_MODULES = ['phpbb3_prosilver_crawler.spiders']
#NEWSPIDER_MODULE = 'phpbb3_prosilver_crawler.spiders'

SPIDER_SETTINGS = {
    'ForumSpider': 'spider_settings.ForumSpider',
    'TopicSpider': 'spider_settings.TopicSpider',
}

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)'
DOWNLOAD_HANDLERS = {'s3': None,}
CONCURRENT_REQUESTS=1

#GET requests will randomly be assigned every 0.5x-1.5x the DOWNLOAD_DELAY in seconds. This means we will have a maximum of 750 GET requests every 16,6667 hours. 
#the spiders will be started using JOBDIR to resume and stop when needed.
DOWNLOAD_DELAY=5

TELNETCONSOLE_ENABLED=False

#Stop after 76 requests
#CLOSESPIDER_PAGECOUNT=76

ITEM_PIPELINES = {
    'phpbb3_prosilver_crawler.pipelines.DatabasePipeline': 300,
}

LOG_LEVEL='INFO'

##############################
# Crawler specific settings
#
# CHANGE ME
##############################

WEBSITE_USERNAME=
WEBSITE_PASSWORD=
WEBSITE_URL=

DB_NAME=
DB_USERNAME=
DB_PASSWORD=
DB_HOST=

