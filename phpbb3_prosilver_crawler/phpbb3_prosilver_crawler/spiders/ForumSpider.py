##############################################################################
#
# Crawler for PHPBB3 Pro Silver Theme - 6 March 2018
#  Crawls topics in forums
#
# Syntax: sudo scrapy runspider ForumSpider.py
#
##############################################################################

import logging
import scrapy
from phpbb3_prosilver_crawler.items import Topic
from phpbb3_prosilver_crawler.items import Forum
from DatabaseConnector import DatabaseConnector
from random import randint
import time
import urllib2
from scrapy.utils.project import get_project_settings

class ForumSpider(scrapy.Spider):
    name = 'ForumSpider'

    #website specifics
    USERNAME=""
    PASSWORD=""
    WEBSITE_URL=""

    #phpbb3 prosilver specifics
    LOGIN_PAGE_URL=""
    LOGIN_PAGE='ucp.php?mode=login'
    VIEWTOPIC_PAGE="viewtopic.php"
    VIEWFORUM_PAGE="viewforum.php"
    INDEX_PAGE="index.php"
    URL_FORUM_ARGUMENT="f"
    URL_TOPIC_ARGUMENT="t"
    URL_VIEW_PRINT_ARGUMENT='view=print'
    databaseConnector=DatabaseConnector()

    #selectors
    CURRENT_PAGE_SELECTOR=".pagination > a > strong ::text"
    NEXT_PAGE_SELECTOR=".display-options a.right-box::attr(href)"
    FORUMS_SELECTOR=".forabg .forumtitle"
    FORUM_TITLE_SELECTOR="::text"
    FORUM_HREF_SELECTOR="::attr(href)"
    TOPICS_SELECTOR=".forumbg .topictitle"
    TOPIC_TITLE_SELECTOR="::text"
    TOPIC_HREF_SELECTOR="::attr(href)"

    FORUM_URLS=[]

    def __init__(self):
     settings = get_project_settings()
     self.USERNAME=settings.get('WEBSITE_USERNAME')
     self.PASSWORD=settings.get('WEBSITE_PASSWORD')
     self.WEBSITE_URL=settings.get('WEBSITE_URL')
     self.LOGIN_PAGE_URL = self.WEBSITE_URL+self.LOGIN_PAGE
     #forum urls to crawl
     self.FORUM_URLS=[self.WEBSITE_URL+self.VIEWFORUM_PAGE+"?"+self.URL_FORUM_ARGUMENT+"=1"]

    def start_requests(self):
     yield scrapy.Request(url=self.LOGIN_PAGE_URL, callback=self.login)

    def login(self,response):
      return scrapy.FormRequest.from_response(response,formdata={'username': self.USERNAME, 'password': self.PASSWORD,'login': 'login', 'redirect':self.INDEX_PAGE}, callback=self.afterLogin)

    def afterLogin(self, response):
        if "Logout" in response.body:
            logging.getLogger().info("Successfully logged in. Let's start crawling!")
            #crawl each forum
            for forumUrl in self.FORUM_URLS:
   	     yield scrapy.Request(url=forumUrl, callback=self.parse)
        else:
            logging.getLogger().info("Login failed.")
        return

    def getTopicIdFromUrl(self,url,forumId):
     return url.replace(self.WEBSITE_URL+self.VIEWTOPIC_PAGE+"?"+self.URL_FORUM_ARGUMENT+"="+forumId+"&"+self.URL_TOPIC_ARGUMENT+"=","")

    def getForumIdFromUrl(self,url):
     return url.replace(self.WEBSITE_URL+self.VIEWFORUM_PAGE+"?"+self.URL_FORUM_ARGUMENT+"=","")

    def skipCallback(self,url):
     pass

    def parseTopicPage(self,response):
     currentForumId=response.meta["forumId"]
     topicItemId=response.meta["id"]
     topicItemTitle=response.meta["title"]
     topicItemUrl=response.meta["url"]
     topicItemContentHtml=response.body
     topicItem=Topic(id=topicItemId,forumId=currentForumId,title=topicItemTitle,content=topicItemContentHtml,url=topicItemUrl)
     logging.getLogger().info("Sending to pipeline topic ID: " + topicItem['id'])
     yield topicItem

    def parse(self, response):
        forumUrl=response.request.url
        currentForumId=forumUrl[36:].split('&')[0].replace(self.URL_FORUM_ARGUMENT+'=','')
        currentPage=response.css(self.CURRENT_PAGE_SELECTOR)
        #save the whole page

        #crawl page for forums, only if its the first page
	forums=response.css(self.FORUMS_SELECTOR)
        if currentPage:
         currentPage=currentPage.extract()[0]

        if currentPage == '1' or not currentPage:
         if forums:
          for forum in forums:
           forumItemTitle=forum.css(self.FORUM_TITLE_SELECTOR).extract()[0]
           forumItemUrl=self.WEBSITE_URL+(forum.css(self.FORUM_HREF_SELECTOR).extract()[0])[2:]
           forumItemId=self.getForumIdFromUrl(forumItemUrl)
           forumItem=Forum(id=forumItemId,title=forumItemTitle,url=forumItemUrl)
           logging.getLogger().info("Sending to pipeline forum ID: " + forumItem['id'])
           yield forumItem
           yield scrapy.Request(forumItemUrl,callback=self.parse)

        #crawl page for topics, in case they exist
        topics=response.css(self.TOPICS_SELECTOR)
        if topics:
         for topic in topics:
      	  topicItemTitle=topic.css(self.TOPIC_TITLE_SELECTOR).extract()[0]
          topicItemUrl=self.WEBSITE_URL+(topic.css(self.TOPIC_HREF_SELECTOR).extract()[0])[2:]
          topicItemId=self.getTopicIdFromUrl(topicItemUrl,currentForumId)
          topicItemContentHtml='N/A'
#          responseTopicPage=(yield scrapy.Request(topicItemUrl+'&'+self.URL_VIEW_PRINT_ARGUMENT,callback=self.parseTopicPage,dont_filter = True))
          yield scrapy.Request(topicItemUrl+'&'+self.URL_VIEW_PRINT_ARGUMENT,callback=self.parseTopicPage,meta={"id": topicItemId,"title":topicItemTitle,"url":topicItemUrl,"forumId":currentForumId},dont_filter = True)

        #follow to topic's next page or quit
        nextPageRelativeUrl = response.css(self.NEXT_PAGE_SELECTOR).extract()
        if nextPageRelativeUrl:
         nextPageRelativeUrl=nextPageRelativeUrl[0]
         nextPageRelativeUrl=nextPageRelativeUrl[2:]
         nextPageAbsoluteUrl = self.WEBSITE_URL+nextPageRelativeUrl
         time.sleep(randint(1,3))
         yield scrapy.Request(nextPageAbsoluteUrl,callback=self.parse,dont_filter = True)
	else:
	 logging.getLogger().info("Finished crawling Forum "+currentForumId)

        return
