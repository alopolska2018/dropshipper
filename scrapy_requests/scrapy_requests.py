import requests, json
import subprocess, os


class ScrapyRequests():
    def __init__(self):
        self.cookies = self.get_cookies

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

    def run_cat_spider(self):
        pass

    def run_products_spider(self):
        pass


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
