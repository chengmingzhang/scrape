# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class BiqugePipeline:
    def process_item(self, item, spider):
        return item

class SaveToMongodb:
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.collection = self.client['biquge98']['xuanhuan_and_xiuzhen']

    def process_item(self, item, spider):
        if not self.collection.find_one(item):
            self.collection.insert_one(item)
            print(f"{ item['name'] }保存到MongoDB数据库中完成......")
            return item
        print(f"{ item['name']}已经在库，自动过滤......")

    def close_spider(self, spider):
        self.client.close()



