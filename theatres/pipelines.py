# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from daterangeparser import parse
import datetime

class ParseDatePipeline(object):
    def process_item(self, item, spider):
        start, end = parse(item['date'])
        item['start'] = start.strftime('%Y-%m-%d %H:%M:%S')
        if not end == None:
          item['end'] = end.strftime('%Y-%m-%d %H:%M:%S')
        else:
          item['end'] = "null"
      
        return item

class AddLocationPipeline(object):
  def process_item(self, item, spider):
    item['location'] = spider.location
    
    return item
    
    
from twisted.enterprise import adbapi
from scrapy import log
import datetime

import pymysql
pymysql.install_as_MySQLdb()

import MySQLdb.cursors

class SQLStorePipeline(object):

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='events',
                user='root', passwd='root', port=8889, host="127.0.0.1", cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8', use_unicode=True)

    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)

        return item

    def _conditional_insert(self, tx, item):
        tx.execute("insert into events (title, url, description, start_date, end_date, location) "
              "values (%s, %s, %s, %s, %s, %s)",
              (item['name'], item['url'], item['desc'], item['start'], item['end'], item['location']))
        log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)