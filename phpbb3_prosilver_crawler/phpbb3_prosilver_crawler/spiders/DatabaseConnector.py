from phpbb3_prosilver_crawler.items import Topic
import logging
import ConfigParser
import pymysql
import os.path
import traceback
import sys
from scrapy.utils.project import get_project_settings

class DatabaseConnector:
 DB_NAME=""
 DB_URL=""
 DB_USERNAME=""
 DB_PASSWORD=""
 connection=""
 connectionCursor=""

 def __init__(self):
  settings = get_project_settings()
  self.DB_NAME=settings.get('DB_NAME')
  self.DB_URL=settings.get('DB_HOST')
  self.DB_USERNAME=settings.get('DB_USERNAME')
  self.DB_PASSWORD=settings.get('DB_PASSWORD')
#  self.open()

 def close(self):
   self.connection.close()

 def open(self):
   try:
    self.connection = pymysql.connect(user=self.DB_USERNAME, password=self.DB_PASSWORD,host=self.DB_URL,database=self.DB_NAME,charset='utf8')
    self.connectionCursor = self.connection.cursor()
    self.connectionCursor.execute('SET NAMES utf8;')
    self.connectionCursor.execute('SET CHARACTER SET utf8;')
    self.connectionCursor.execute('SET character_set_connection=utf8;')
   except pymysql.MySQLError as e:
    logging.getLogger().info('Error {} - {!r} '.format(e.args[0], e.args[1].decode("utf-8")))

 def insertIntoPosts(self,post):
    try:
     self.connectionCursor.execute("""INSERT INTO POSTS (POST_ID,TITLE,DATE,AUTHOR,CONTENT_HTML,URL,FORUM_ID,TOPIC_ID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(post['id'],post['title'],post['date'],post['author'],post['content'],post['url'],post['forumId'],post['topicId']))
     self.connection.commit()
    except pymysql.MySQLError as e:
     logging.getLogger().info('Error {} - {!r} '.format(e.args[0], e.args[1].decode("utf-8")))

 def insertIntoTopics(self,topic):
    try:
     self.connectionCursor.execute("""INSERT INTO TOPICS (TOPIC_ID,FORUM_ID,TITLE,CONTENT_HTML,URL) VALUES (%s,%s,%s,%s,%s)""",(topic['id'],topic['forumId'],topic['title'],topic['content'],topic['url']))
     self.connection.commit()
    except pymysql.MySQLError as e:
     logging.getLogger().info('Error {} - {!r} '.format(e.args[0], e.args[1].decode("utf-8")))

 def insertIntoForums(self,forum):
   try:
    self.connectionCursor.execute("""INSERT INTO FORUMS (FORUM_ID,TITLE,URL) VALUES (%s,%s,%s)""",(forum['id'],forum['title'],forum['url']))
    self.connection.commit()
   except pymysql.MySQLError as e:
    logging.getLogger().info('Error {} - {!r} '.format(e.args[0], e.args[1].decode("utf-8")))

 def selectAllTopics(self):
   results = ""
   try:
    self.connectionCursor.execute("""SELECT TOPIC_ID,FORUM_ID,TITLE,URL FROM TOPICS""")
    results = self.connectionCursor.fetchall()
    topics=[]
    for row in results:
      topicId=row[0]
      forumId=row[1]
      title=row[2]
      url=row[3]
      topic=Topic(id=topicId,forumId=forumId,title=title,url=url)
      topics.append(topic)
   except pymysql.MySQLError as e:
    logging.getLogger().info('Error {} - {!r} '.format(e.args[0], e.args[1].decode("utf-8")))
   return topics
