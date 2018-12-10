# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re, pymongo, time
from collections import Counter

class QuotePipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.list = []
    

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )
    
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    
    def process_item(self, item, spider):
        if spider.name == 'quotes':
            self.list.append(item['author'])
        return item

    def close_spider(self, spider):
        if spider.name == 'quotes':
            self.count = Counter(self.list).most_common()
            self.db['author'].insert_many([{'author': i[0], 'count': i[1], 'query_date': time.time()} for i in self.count])
        self.client.close()
