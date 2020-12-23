from ali_scrapy.ali.ali.spiders.cat_spider import CatSpider
from ali_scrapy.ali.ali.spiders.products_spider import ProductSpider

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


class Scraper:
    def __init__(self):
        settings_file_path = 'ali.ali.settings' # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())

    def run_cat_spider(self, cat_id, num_of_result):
        self.process.crawl(CatSpider, cat_id=cat_id, num_of_result=num_of_result)
        self.process.start()

    def run_products_spider(self, allegro_cat_id):
        self.process.crawl(ProductSpider, allegro_cat_id=allegro_cat_id)
        self.process.start()
