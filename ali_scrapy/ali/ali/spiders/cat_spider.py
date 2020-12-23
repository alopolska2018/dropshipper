import scrapy
import js2xml
import json
from ..items import AliItem
class CatSpider(scrapy.Spider):

    name = "cat"
    def __init__(self, cat_id=None, num_of_result=None, *args, **kwargs):
        super(CatSpider, self).__init__(*args, **kwargs)
        self.cat_id = cat_id
        self.num_of_result = num_of_result
        self.clear_log()
        self.url = 'https://pl.aliexpress.com/af/category/{}.html?trafficChannel=af&CatId=200010062&ltype=affiliate&isFreeShip=y&isFavorite=y&SortType=total_tranpro_desc&page=1&groupsort=1&isrefine=y'.format(self.cat_id)
        self.cookies = self.get_cookies()
        self.counter = 2

    def get_cookies(self):
        cookies = {}
        with open('cookies.json') as json_file:
            data = json.load(json_file)
            for item in data:
                name = item['name']
                value = item['value']
                cookies[name] = value
        return cookies

    def get_ali_url(self, product_id):
        url = 'https://pl.aliexpress.com/item/{}.html'.format(product_id)
        return url

    def get_urls_to_scrape(self, products_json):
        urls_to_scrape = []
        for item in products_json:
            product_id = item['productId']
            url = self.get_ali_url(product_id)
            urls_to_scrape.append(url)
        return urls_to_scrape

    def save_urls_to_file(self, urls):
        with open('urls_to_scrape.txt', 'a') as f:
            f.writelines("%s\n" % url for url in urls)

    def clear_log(self):
        with open('urls_to_scrape.txt', 'w') as f:
            pass

    def start_requests(self):
        start_url = self.url + '&page=1'
        yield scrapy.Request(url=start_url, callback=self.parse, cookies=self.cookies)

    def parse(self, response):
        # selector = scrapy.Selector(text=html, type="html")
        txt = response.text
        #for all auctons on a page '/html/body/script[7]'
        start_phrase = '"items":'
        end_phrase = '"refineCategory"'
        products = txt[txt.find(start_phrase) + len(start_phrase):txt.rfind(end_phrase)]
        products = products[:-1]
        products_json = json.loads(products)
        urls_to_scrape = self.get_urls_to_scrape(products_json)
        self.save_urls_to_file(urls_to_scrape)

        next_page = self.url + '&page={}'.format(self.counter)
        if self.counter <= self.num_of_result:
            self.counter += 1
            yield response.follow(next_page, callback=self.parse, cookies=self.cookies)

