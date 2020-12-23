# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AliItem(scrapy.Item):
    # define the fields for your item here like:
    products = scrapy.Field()
    desc_url = scrapy.Field()
    description = scrapy.Field()
    product_id = scrapy.Field()
    category_id = scrapy.Field()
    images = scrapy.Field()
    shop_info = scrapy.Field()
    num_of_sold_items = scrapy.Field()
    product_name = scrapy.Field()
    products_specs = scrapy.Field()
    shipping_list = scrapy.Field()
    allegro_category_id = scrapy.Field()
    # woocommerce_id = scrapy.Field()