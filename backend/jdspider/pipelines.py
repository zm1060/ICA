import datetime
import logging

import pymongo

from jdspider.settings import MONGO_URI, MONGO_DATABASE


class JDspiderPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=MONGO_URI,
            mongo_db=MONGO_DATABASE
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.task_db = self.client['users']

    def close_spider(self, spider):
        # 从爬虫对象中获取统计信息、task_id和user_id
        stats_info = spider.crawler.stats.get_stats()
        task_id = spider.task_id

        # 获取当前时间作为finish_time，并将其添加到stats_info字典中
        finish_time = datetime.datetime.now()
        stats_info['finish_time'] = finish_time

        # 将统计信息（包括task_id和user_id）写入MongoDB
        print(f"Stats info in pipeline: {stats_info}")
        self.task_db['tasks'].update_one({'task_id': task_id}, {'$set': {'stats': stats_info}}, upsert=True)
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'JDspider':
            collection_name = 'jd_products'
            collection = self.db[collection_name]
            data = {
                'name': item['name'],
                'url': item['url'],
                'content': item['content']
            }
            collection.insert_one(data)
        return item


class JDcommentPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.task_db = self.client['users']

    def close_spider(self, spider):
        # 从爬虫对象中获取统计信息、task_id和user_id
        stats_info = spider.crawler.stats.get_stats()
        task_id = spider.task_id

        # 获取当前时间作为finish_time，并将其添加到stats_info字典中
        finish_time = datetime.datetime.now()
        stats_info['finish_time'] = finish_time

        # 将统计信息（包括task_id和user_id）写入MongoDB
        print(f"Stats info in pipeline: {stats_info}")
        self.task_db['tasks'].update_one({'task_id': task_id}, {'$set': {'stats': stats_info}}, upsert=True)
        self.client.close()


    def process_item(self, item, spider):
        if spider.name == 'JDcommentspider':
            collection_name = str(spider.task_id)
            collection = self.db[collection_name]
            data = {
                'name': item['name'],
                'url': item['url'],
                'date': item['date'],
                'content': item['content']
            }
            collection.insert_one(data)
        return item