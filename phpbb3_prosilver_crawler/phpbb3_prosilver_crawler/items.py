# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Forum(scrapy.Item):
   id=scrapy.Field(default="")
   title=scrapy.Field(default="")
   url=scrapy.Field(default="")
   pass

class Topic(scrapy.Item):
   id=scrapy.Field(default="")
   forumId=scrapy.Field(default="")
   title=scrapy.Field(default="")
   content=scrapy.Field(default="")
   url=scrapy.Field(default="")
   pass

class Post(scrapy.Item):
   author=scrapy.Field(default="")
   date=scrapy.Field(default="")
   content=scrapy.Field(default="")
   title=scrapy.Field(default="")
   url=scrapy.Field(default="")
   id=scrapy.Field(default="")
   forumId=scrapy.Field(default="")
   topicId=scrapy.Field(default="")
   pass

class Phpbb3ProsilverCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
