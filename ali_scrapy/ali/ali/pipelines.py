# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError


class AliPipeline(object):

    def __init__(self):
        self.client = MongoClient()
        self.client = MongoClient('localhost', 27017)
        db = self.client['ali']
        self.collection = db['ali']

    def process_item(self, item, spider):
        if spider.name == 'cat_spider':
            return item
        if spider.name == 'products_spider':
            print('Processing product_id {}'.format(item['product_id']))
            try:
                db_id = self.collection.insert_one({"_id": item['product_id'], "woocommerce_id": 0, "data": item}).inserted_id
                print('Successfully added product_id: {} to database.'.format(db_id))
            except DuplicateKeyError:
                print('Unable to add product_id {}. Id already exist in database.'.format(item['product_id']))