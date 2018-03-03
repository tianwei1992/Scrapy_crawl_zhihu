# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
class MongoPipeline(object):
    def process_item(self, item, spider):
        print('insert db')
        self.db['user'].update({'url_token':item['url_token']},{'$set':item},True)
        """这一句用update去重很有必要，在这里必然会有大量的抽工夫用户，True表示重复就更新，不重复就插入" 
        第一个参数是判断重复的条件，第二个参数是最新的数据
        """

    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri=mongo_uri
        self.mongo_db=mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.mongo_uri)
        self.db=self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()


