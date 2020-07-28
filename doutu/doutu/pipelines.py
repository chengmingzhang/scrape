# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class DoutuPipeline:
    def process_item(self, item, spider):
        return item

class MongoPipeline:
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host='47.113.85.28', port=27017)
        self.collections = self.client['pics']['doutula']

    def process_item(self, item, spider):
        self.collections.update({'name': item['name'], 'url_images': item['image_urls']}, {'$set': item}, upsert=True)
        print(f"{item['name']}保存到mongodb完成......")
        return item

    def close_spider(self, spider):
        self.client.close()

class DoutuPicsDownloaderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        url =  item['image_urls']
        yield scrapy.Request(url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        file_name = item['name'] + '.jpg'
        return file_name
