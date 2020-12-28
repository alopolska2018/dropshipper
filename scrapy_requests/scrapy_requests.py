import requests, json
import subprocess, os
from requests.exceptions import HTTPError



class ScrapyRequests():
    def __init__(self):
        self.REQUEST_URL = 'http://localhost:3000/crawl.json'

    # def run_scrapyart_server(self):
    #     path = os.path.join(os.getcwd(), 'run_scrapyrt.bat')
    #     subprocess.Popen([r'{}'.format(path)])


    def get_cookies(self):
        cookies = {}
        with open('cookies.json') as json_file:
            data = json.load(json_file)
            for item in data:
                name = item['name']
                value = item['value']
                cookies[name] = value
        return cookies

    def generate_url_for_cat_spider(self, aliexpress_cat_id):
        url = f'https://pl.aliexpress.com/af/category/{aliexpress_cat_id}.html?trafficChannel=af&CatId=200010062&ltype=affiliate&isFreeShip=y&isFavorite=y&SortType=total_tranpro_desc&page=1&groupsort=1&isrefine=y&page=1'
        return url


    def create_request_body_products_spider(self, url, allegro_cat_id):
        request = {'url': url, 'callback': 'parse', 'cookies': self.get_cookies()}

        body = {'spider_name': 'products_spider', 'allegro_cat_id': allegro_cat_id, 'request': request}
        return json.dumps(body)

    def create_request_body_cat_spider(self, aliexpress_cat_id, pages):
        request = {'callback': 'parse', 'cookies': self.get_cookies()}

        body = {'start_requests': True, 'spider_name': 'cat_spider', 'aliexpress_cat_id': aliexpress_cat_id, 'pages': pages, 'request': request}
        return json.dumps(body)

    def run_products_spider(self, url, allegro_cat_id):
        body = self.create_request_body_products_spider(url, allegro_cat_id)
        try:
            response = requests.post(self.REQUEST_URL, data=body)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print('Success!')
            print(response.text)

    def run_cat_spider_post(self, aliexpress_cat_id, pages):
        body = self.create_request_body_cat_spider(aliexpress_cat_id, pages)
        try:
            response = requests.post(self.REQUEST_URL, data=body)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print('Success!')
            print(response.text)

    def run_cat_spider_get(self, aliexpress_cat_id, pages):
        params = {
            'spider_name': 'cat_spider',
            'start_requests': True,
            'cat_id': aliexpress_cat_id,
            'pages': pages
        }
        try:
            response = requests.get(self.REQUEST_URL, params)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print('Success!')
            print(response.text)

# json1 = {
#     "request": {
#         "url": "http://localhost:3000",
#         "meta": {
#             "cat_id": "200000669",
#             "num_of_result": "1",
#         },
#         "callback": "parse_product",
#         "dont_filter": "True",
#     },
#     "spider_name": "cat"
# }
#
# def get_cookies():
#     cookies = {}
#     with open('cookies.json') as json_file:
#         data = json.load(json_file)
#         for item in data:
#             name = item['name']
#             value = item['value']
#             cookies[name] = value
#     return cookies
#
#
# # meta_dict = {}
# # meta_dict['allegro_cat_id'] = 1
# # meta_dict['cat_id'] = 200000669
# # meta_dict['num_of_result'] = 1
#
# urls = ['https://pl.aliexpress.com/item/32382009825.html', 'https://pl.aliexpress.com/item/32726480756.html', 'https://pl.aliexpress.com/item/32915152556.html']
#
# request = {}
# request['url'] = 'https://pl.aliexpress.com/item/32915152556.html'
# request['callback'] = 'parse'
# request['cookies'] = get_cookies()
# # request['meta'] = meta_dict
# all_in_one = {}
# all_in_one['spider_name'] = 'products_spider'
# all_in_one['allegro_cat_id'] = 1551
# all_in_one['request'] = request
#
#
# bjson = json.dumps(all_in_one)
#
#
#
# a = requests.post(url='http://localhost:3000/crawl.json', data=bjson)
# print(a.text)
