# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from spiders.DatabaseConnector import DatabaseConnector
from items import Forum
from items import Topic
from items import Post

class DatabasePipeline(object):
 databaseConnector=""

 def open_spider(self, spider):
    self.databaseConnector=DatabaseConnector()
    self.databaseConnector.open()

 def close_spider(self, spider):
    self.databaseConnector.close()

 def process_item(self, item, spider):
    if isinstance(item, Forum):
     self.databaseConnector.insertIntoForums(item)
    elif isinstance(item, Topic):
     self.databaseConnector.insertIntoTopics(item)
    elif isinstance(item, Post):
     self.databaseConnector.insertIntoPosts(item)
    else:
     logging.getLogger().info("Not a Forum,Topic or Post Item")

# def __init__(self):

