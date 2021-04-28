# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3
import pymongo

from notifier.spiders.info import *


class MongodbPipeline:
    collection_name = "Grades"

    def __init__(self):
        self.client = None
        self.db = None

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client["Notifier"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item


class SQLitePipeline:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def open_spider(self, spider):
        self.connection = sqlite3.connect("notifier.sqlite")
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute("""
                        CREATE TABLE grades(
                            course_code TEXT,
                            course_title TEXT,
                            section TEXT,
                            units INTEGER,
                            midterm_grade DOUBLE,
                            final_grade DOUBLE
                        )
                    """)
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO grades 
            (course_code, course_title, section, units, midterm_grade, final_grade) 
            VALUES(?,?,?,?,?,?)
        """, (
            item["Course Code"],
            item["Course Title"],
            item["Section"],
            item["Units"],
            item["Midterm"],
            item["Final"]
        ))
        self.connection.commit()
        return item
