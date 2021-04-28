# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo

from notifier.spiders.info import *


class MongodbPipeline:
    collection_name = "Grades"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client["Notifier"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item
