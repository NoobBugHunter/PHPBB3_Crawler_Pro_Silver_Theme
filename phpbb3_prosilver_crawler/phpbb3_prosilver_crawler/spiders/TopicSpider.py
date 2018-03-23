#########################################################
#
# Crawler for PHP3BB Pro Silver Theme - 6 March 2018
#  crawls posts in a topic
#
# syntax: sudo scrapy runspider TopicSpider.py
#
#########################################################

import logging
import scrapy
from phpbb3_prosilver_crawler.items import Post
from phpbb3_prosilver_crawler.items import Topic
from random import randint
import time
from DatabaseConnector import DatabaseConnector
from scrapy.utils.project import get_project_settings

class TopicSpider(scrapy.Spider):
    name = 'TopicSpider'

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

    databaseConnector=DatabaseConnector()

    #Page selectors
    CURRENT_PAGE_SELECTOR=".pagination > a > strong ::text"
    NEXT_PAGE_SELECTOR=".display-options a.right-box::attr(href)"

    #POST selectors
    POST_AUTHORS_SELECTOR=".post > .inner > .postbody > .author > strong > a ::text"
    POST_DATES_SELECTOR=".post > .inner > .postbody > .author"
    POST_CONTENTS_SELECTOR='.post > .inner > .postbody > .content'
    POST_TITLES_SELECTOR='.post > .inner > .postbody > h3 > a ::text'
    POST_URLS_SELECTOR='.post > .inner > .postbody > .author > a ::attr(href)'
    POST_IDS_SELECTOR='.post > .inner > .postbody > h3 > a ::attr(href)'

    #TOPIC selectors
    TOPIC_URL_SELECTOR='#page-body > h2 > a ::attr(href)'

    def __init__(self):
     settings = get_project_settings()
     self.USERNAME=settings.get('WEBSITE_USERNAME')
     self.PASSWORD=settings.get('WEBSITE_PASSWORD')
     self.WEBSITE_URL=settings.get('WEBSITE_URL')
     self.LOGIN_PAGE_URL = self.WEBSITE_URL+self.LOGIN_PAGE

    def getForumIdFromUrl(self,url):
     return url.replace(self.WEBSITE_URL+self.VIEWTOPIC_PAGE+"?","").split('&')[0].replace(self.URL_FORUM_ARGUMENT+'=','')

    def getTopicIdFromUrl(self,url):
     return url.replace(self.WEBSITE_URL+self.VIEWTOPIC_PAGE+"?","").split('&')[1].replace(self.URL_TOPIC_ARGUMENT+'=','')

    def start_requests(self):
     yield scrapy.Request(url=self.LOGIN_PAGE_URL, callback=self.login)

    def login(self,response):
      return scrapy.FormRequest.from_response(response,formdata={'username': self.USERNAME, 'password': self.PASSWORD,'login': 'login', 'redirect':self.INDEX_PAGE}, callback=self.afterLogin)

    def afterLogin(self, response):
        if "Logout" in response.body:
            logging.getLogger().info("Successfully logged in. Let's start crawling!")
            #crawl each forum
	    self.databaseConnector.open()
            topics=self.databaseConnector.selectAllTopics()
	    for topic in topics:
             yield scrapy.Request(url=topic['url'], callback=self.parse)
        else:
            logging.getLogger().info("Login failed.")
        return

    def parse(self, response):
        topicUrl=response.request.url
        forumId=self.getForumIdFromUrl(topicUrl)
        topicId=self.getTopicIdFromUrl(topicUrl)

        #parse authors and contents
        authors=response.css(self.POST_AUTHORS_SELECTOR).extract()
        dates=response.css(self.POST_DATES_SELECTOR).xpath('text()[position()=2]')
        contents=response.css(self.POST_CONTENTS_SELECTOR)
	titles=response.css(self.POST_TITLES_SELECTOR)
	urls=response.css(self.POST_URLS_SELECTOR)
	ids=response.css(self.POST_IDS_SELECTOR)

        lastPost=len(authors)
        i=0

        #iterate through posts and submit to DB
	while (i < lastPost):
         author=authors[i]
         date=dates[i].extract()[3:]
         content=""
         nodes=contents[i].xpath('node()')
         for node in nodes:
          content+=node.extract()
         title=titles[i].extract()
	 url=self.WEBSITE_URL+urls[i].extract()[2:]
	 id=ids[i].extract()[2:]
	 postItem=Post(id=id, title=title, date=date, author=author, content=content, url=url,forumId=forumId,topicId=topicId)
	 logging.getLogger().info("Committing post ID: "+postItem['id'])
         yield postItem
	 i+=1

        #follow to topic's next page or quit
        nextPageRelativeUrl = response.css(self.NEXT_PAGE_SELECTOR).extract()
        if nextPageRelativeUrl:
         nextPageRelativeUrl=nextPageRelativeUrl[0]
         nextPageRelativeUrl=nextPageRelativeUrl[2:]
         nextPageAbsoluteUrl = self.WEBSITE_URL+nextPageRelativeUrl
         time.sleep(randint(1,3))
         yield scrapy.Request(nextPageAbsoluteUrl,callback=self.parse,dont_filter = True)
        else:
         logging.getLogger().info("Finished crawling Topic "+topicId)
        return
