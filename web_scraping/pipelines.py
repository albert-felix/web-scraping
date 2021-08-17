# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class WebScrapingPipeline:
    def process_item(self, item, spider):
        return item


class SmartPhonesPipeline:

    def __init__(self):
        self.create_db()
        self.create_table()

    def create_db(self):
        self.conn = sqlite3.connect('scrapy.db')
        self.cur = self.conn.cursor()
    
    def create_table(self):
        self.cur.execute("DROP TABLE IF EXISTS smartphones")
        self.cur.execute("CREATE TABLE smartphones (name text, price text, imgurl text)")

    def insert_data(self, item):
        name = item['name']
        price = item['price']
        img_url = item['img_url']

        self.cur.execute("INSERT INTO smartphones VALUES (?, ?, ?)", (name, price, img_url))
        self.conn.commit()

    def process_item(self, item, spider):
        self.insert_data(item)
        return item

    def close_spider(self, spider):
        self.conn.close()