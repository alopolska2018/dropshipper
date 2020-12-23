import scrapy
import js2xml
from ..items import AliItem
from inscriptis import get_text
import requests
import os, json

class ProductSpider(scrapy.Spider):
    name = "products_spider"

    def __init__(self, allegro_cat_id=None, *args, **kwargs):
        super(ProductSpider, self).__init__(*args, **kwargs)
        self.allegro_cat_id = allegro_cat_id
        print(self.allegro_cat_id)
        self.num_of_attr = 0
        self.items = AliItem()

    def get_cookies(self):
        cookies = {}
        with open('cookies.json') as json_file:
            data = json.load(json_file)
            for item in data:
                name = item['name']
                value = item['value']
                cookies[name] = value
        return cookies

    def get_urls_from_file(self):
        urls = []
        with open('urls_to_scrape.txt', 'r') as f:
            for line in f:
                urls.append(line.strip())
        return urls

    def get_category_id(self, data):
        return data['categoryId']

    def get_images(self, data):
        return data['imagePathList']

    def get_shop_info(self, data):
        shop_info = {}
        shop_info['shop_url'] = data['storeURL']
        shop_info['shop_location'] = data['detailPageUrl']
        shop_info['shop_followers'] = data['followingNumber']
        shop_info['shop_followers'] = data['followingNumber']
        shop_info['shop_positive_rate'] = data['positiveRate']
        shop_info['storeName'] = data['storeName']
        return shop_info

    def get_product_specs(self, data):
        specs = {}
        for item in data['props']:
            attr_name = item['attrName']
            attr_value = item['attrValue']
            specs[attr_name] = attr_value
        return specs

    def get_num_of_sold_items(self, data):
        try:
            return data['tradeCount']
        except KeyError:
            return 0

    def get_product_name(self, data):
        return data['subject']

    def parse_colour_property(self, item, product):
        img_url = item['skuPropertyImagePath']
        # TODO check if better fields exist for the colour name
        colour = item['propertyValueDisplayName']
        product['colour'] = colour
        product['img_url'] = img_url
        return product

    def parse_size_property(self, item, product):
        size = item['propertyValueDisplayName']
        product['size'] = size
        return product

    def parse_length_property(self, item, product):
        length = item['propertyValueDisplayName']
        product['length'] = length
        return product

    def parse_shipping_property(self, item, product):
        # TODO EXCPTION, DO NO CREATE PRODUCT WITHOUT SHIPPNG FROM CHINA
        send_goods_country_code = item['skuPropertySendGoodsCountryCode']
        product['shipping'] = send_goods_country_code
        return product

    def get_all_sku_property_ids(self, data):
        sku_property_id_list = []
        for item in data:
            sku_property_id = item['skuPropertyId']
            sku_property_id_list.append(sku_property_id)
        return sku_property_id_list

    def create_sku_property_map(self):
        sku_map = {}
        sku_map['14'] = 'colour'
        sku_map['5'] = 'size'
        sku_map['200001036'] = 'length'
        sku_map['200007763'] = 'shipping'
        return sku_map

    def create_products(self, data):
        import itertools

        # attributes of auction can be in different order such as shipping, colour, size or colour, size, shipping
        # sku_property_id defines current attr. id 14 = colour, id 5 = size, id 200001036 = lenght, id 200007763 = shipping
        products = {}
        self.num_of_attr = len(data)
        product_id = self.items['product_id']
        product_id = str(product_id)
        sku_map = self.create_sku_property_map()

        if self.num_of_attr == 1:
            sku_property_id1 = data[0]['skuPropertyId']
            for item in data[0]['skuPropertyValues']:
                product = {}
                if sku_property_id1 == 14:
                    product = self.parse_colour_property(item, product)
                    product['attr1_value'] = item['propertyValueId']
                elif sku_property_id1 == 5:
                    product = self.parse_size_property(item, product)
                    product['attr1_value'] = item['propertyValueId']
                elif sku_property_id1 == 200001036:
                    product = self.parse_length_property(item, product)
                    product['attr1_value'] = item['propertyValueId']
                elif sku_property_id1 == 200007763:
                    if not item['skuPropertySendGoodsCountryCode'] == 'CN':
                        raise Exception('Product doesn\'t ship from china')
                    product = self.parse_shipping_property(item, product)
                    product['attr1_value'] = item['propertyValueId']

                property1 = sku_map[str(sku_property_id1)]
                sku = product_id + '-' + product[property1]

                if '.' in sku:
                    sku = sku.replace('.', ',')

                products[sku] = product

        if self.num_of_attr == 2:
            sku_property_id1 = data[0]['skuPropertyId']
            sku_property_id2 = data[1]['skuPropertyId']
            for item1 in data[0]['skuPropertyValues']:
                product = {}
                if sku_property_id1 == 14:
                    product = self.parse_colour_property(item1, product)
                    product['attr1_value'] = item1['propertyValueId']
                elif sku_property_id1 == 5:
                    product = self.parse_size_property(item1, product)
                    product['attr1_value'] = item1['propertyValueId']
                elif sku_property_id1 == 200001036:
                    product = self.parse_length_property(item1, product)
                    product['attr1_value'] = item1['propertyValueId']
                elif sku_property_id1 == 200007763:
                    if not item1['skuPropertySendGoodsCountryCode'] == 'CN':
                        continue
                    product = self.parse_shipping_property(item1, product)
                    product['attr1_value'] = item1['propertyValueId']

                for item2 in data[1]['skuPropertyValues']:
                    if sku_property_id2 == 14:
                        product = self.parse_colour_property(item2, product)
                        product['attr2_value'] = item2['propertyValueId']
                    elif sku_property_id2 == 5:
                        product = self.parse_size_property(item2, product)
                        product['attr2_value'] = item2['propertyValueId']
                    elif sku_property_id2 == 200001036:
                        product = self.parse_length_property(item2, product)
                        product['attr2_value'] = item2['propertyValueId']
                    elif sku_property_id2 == 200007763:
                        if not item1['skuPropertySendGoodsCountryCode'] == 'CN':
                            continue
                        product = self.parse_shipping_property(item2, product)
                        product['attr2_value'] = item2['propertyValueId']

                    property1 = sku_map[str(sku_property_id1)]
                    property2 = sku_map[str(sku_property_id2)]
                    if property2 == 'shipping':
                        sku = product_id + '-' + product[property1]
                    elif property1 == 'shipping':
                        sku = product_id + product[property2]
                    else:
                        sku = product_id + '-' + product[property1] + '-' + product[property2]

                    if '.' in sku:
                        sku = sku.replace('.', ',')

                    new_product = {**product}
                    products[sku] = new_product


        if self.num_of_attr == 3:
            sku_property_id1 = data[0]['skuPropertyId']
            sku_property_id2 = data[1]['skuPropertyId']
            sku_property_id3 = data[2]['skuPropertyId']

            for item1 in data[0]['skuPropertyValues']:
                product = {}
                if sku_property_id1 == 14:
                    product = self.parse_colour_property(item1, product)
                    product['attr1_value'] = item1['propertyValueId']
                elif sku_property_id1 == 5:
                    product = self.parse_size_property(item1, product)
                    product['attr1_value'] = item1['propertyValueId']
                elif sku_property_id1 == 200001036:
                    product = self.parse_length_property(item1, product)
                    product['attr1_value'] = item1['propertyValueId']
                elif sku_property_id1 == 200007763:
                    if not item1['skuPropertySendGoodsCountryCode'] == 'CN':
                        continue
                    product = self.parse_shipping_property(item1, product)
                    product['attr1_value'] = item1['propertyValueId']

                for item2 in data[1]['skuPropertyValues']:
                    if sku_property_id2 == 14:
                        product = self.parse_colour_property(item2, product)
                        product['attr2_value'] = item2['propertyValueId']
                    elif sku_property_id2 == 5:
                        product = self.parse_size_property(item2, product)
                        product['attr2_value'] = item2['propertyValueId']
                    elif sku_property_id2 == 200001036:
                        product = self.parse_length_property(item2, product)
                        product['attr2_value'] = item2['propertyValueId']
                    elif sku_property_id2 == 200007763:
                        if not item2['skuPropertySendGoodsCountryCode'] == 'CN':
                            continue
                        product = self.parse_shipping_property(item2, product)
                        product['attr2_value'] = item2['propertyValueId']

                    for item3 in data[2]['skuPropertyValues']:
                        if sku_property_id3 == 14:
                            product = self.parse_colour_property(item3, product)
                            product['attr3_value'] = item3['propertyValueId']
                        elif sku_property_id3 == 5:
                            product = self.parse_size_property(item3, product)
                            product['attr3_value'] = item3['propertyValueId']
                        elif sku_property_id3 == 200001036:
                            product = self.parse_length_property(item3, product)
                            product['attr3_value'] = item3['propertyValueId']
                        elif sku_property_id3 == 200007763:
                            if not item3['skuPropertySendGoodsCountryCode'] == 'CN':
                                continue
                            product = self.parse_shipping_property(item3, product)
                            product['attr3_value'] = item3['propertyValueId']

                        property1 = sku_map[str(sku_property_id1)]
                        property2 = sku_map[str(sku_property_id2)]
                        property3 = sku_map[str(sku_property_id3)]

                        if property3 == 'shipping':
                            sku = product_id + '-' + product[property1] + '-' + product[property2]
                        elif property2 == 'shipping':
                            sku = product_id + '-' + product[property1] + '-' + product[property3]
                        elif property1 == 'shipping':
                            sku = product_id + '-' + product[property2] + '-' + product[property3]
                        else:
                            sku = product_id + '-' + product[property1] + '-' + product[property2] + '-' + product[property3]

                        if '.' in sku:
                            sku = sku.replace('.', ',')

                        new_product = {**product}
                        products[sku] = new_product

        return products


            # for item in zip(data[0]['skuPropertyValues'], data[1]['skuPropertyValues'], data[2]['skuPropertyValues']):
            #     product = {}
            #     product['sku_property_id'] = sku_property_id1
            #     if sku_property_id1 == 14:
            #         product = self.parse_colour_property(item[0], product)
            #         product['attr1_value'] = item['propertyValueId']
            #     elif sku_property_id1 == 5:
            #         product = self.parse_size_property(item[0], product)
            #         product['attr1_value'] = item['propertyValueId']
            #     elif sku_property_id1 == 200001036:
            #         product = self.parse_length_property(item[0], product)
            #         product['attr1_value'] = item['propertyValueId']
            #     elif sku_property_id1 == 200007763:
            #         product = self.parse_shipping_property(item[0], product)
            #         product['attr1_value'] = item['propertyValueId']


    def get_prices(self, price_array, products, lowest_shipping_price):
        price_dict = {}
        for item in price_array:
            sku_attr_id = item['skuPropIds']
            price_dict[sku_attr_id] = item

        for key, value in products.items():
            products_price_dict = {}
            if self.num_of_attr == 1:
                price_dict_key = '{}'.format(value['attr1_value'])
            elif self.num_of_attr == 2:
                price_dict_key = '{},{}'.format(value['attr1_value'], value['attr2_value'])
            elif self.num_of_attr == 3:
                price_dict_key = '{},{},{}'.format(value['attr1_value'], value['attr2_value'], value['attr3_value'])
            try:
                price = price_dict[price_dict_key]['skuVal']['actSkuCalPrice']
            except KeyError:
                price = price_dict[price_dict_key]['skuVal']['skuCalPrice']

            qty = price_dict[price_dict_key]['skuVal']['inventory']
            products_price_dict['price'] = price
            products_price_dict['qty'] = qty

            products[key]['price'] = float(price) + lowest_shipping_price
            products[key]['qty'] = qty
        return products

    def get_shipping_json(self, product_id):
        shipping_json = requests.get('https://pl.aliexpress.com/aeglodetailweb/api/logistics/freight?productId={}&count=1&country=PL'.format(product_id),
                         headers={'Accept': 'application/json',
                                  'Referer': 'https://pl.aliexpress.com/item/{}.html'.format(product_id)}).json()
        return shipping_json

    def get_shipping_details(self, shipping_json):
        shipping_details = []
        for item in shipping_json['body']['freightResult']:
            shipping = {}
            if item['sendGoodsCountry'] == 'CN':
                shipping['shipping_from'] = item['sendGoodsCountry']
                shipping['price_usd'] = item['freightAmount']['value']
                shipping['company'] = item['company']
                shipping['eta'] = item['commitDay']
                shipping['tracking'] = item['tracking']
            shipping_details.append(shipping)
        return shipping_details

    def get_lowest_shipping_price_with_tracking(self, shipping_details):
        price_list = []
        for item in shipping_details:
            if item['tracking'] == True:
                price_list.append(item['price_usd'])
        lowest_price = min(price for price in price_list)
        return lowest_price

    def check_free_shipping(self, shipping_json):
        shipping_list = shipping_json['body']['freightResult']
        for item in shipping_list:
            price = item['freightAmount']['value']
            if price == 0:
                return True
        return False

    def parse_description(self, response):
        # items = AliItem()
        html = response.text
        text = get_text(html)
        self.items['description'] = text
        yield self.items

    def get_description_url(self, data):
        url = data['descriptionUrl']
        return url

    def parse_dict(self, dict):
        products_array = dict['data']['skuModule']['productSKUPropertyList']
        price_array = dict['data']['skuModule']['skuPriceList']
        description_module = dict['data']['descriptionModule']
        shipping_module = dict['data']['shippingModule']
        action_module = dict['data']['actionModule']
        image_module = dict['data']['imageModule']
        store_module = dict['data']['storeModule']
        title_module = dict['data']['titleModule']
        specs_module = dict['data']['specsModule']

        category_id = self.get_category_id(action_module)
        images = self.get_images(image_module)
        shop_info = self.get_shop_info(store_module)
        num_of_sold_items = self.get_num_of_sold_items(title_module)
        product_name = self.get_product_name(title_module)
        products_specs = self.get_product_specs(specs_module)

        self.items['category_id'] = category_id
        self.items['allegro_category_id'] = self.allegro_cat_id
        self.items['images'] = images
        self.items['shop_info'] = shop_info
        self.items['num_of_sold_items'] = num_of_sold_items
        self.items['product_name'] = product_name
        self.items['products_specs'] = products_specs
        # self.items['woocommerce_id'] = 0

        url = self.get_description_url(description_module)
        self.items['desc_url'] = url
        product_id = action_module['productId']
        self.items['product_id'] = product_id

        products = self.create_products(products_array)
        shipping_json = self.get_shipping_json(product_id)
        shipping_list = self.get_shipping_details(shipping_json)
        self.items['shipping_list'] = shipping_list
        try:
            lowest_shipping_price = self.get_lowest_shipping_price_with_tracking(shipping_list)
        except ValueError:
            print('ERROR: None of the shipping methods include tracking')
        products = self.get_prices(price_array, products, lowest_shipping_price)

        return products

    # def start_requests(self):
    #     cookies = self.get_cookies()
    #     yield scrapy.Request(url=url, callback=self.parse, cookies=cookies)

    def parse(self, response):
        global shipping
        js = response.xpath('/html/body/script[11]/text()').extract_first()
        jstree = js2xml.parse(js)
        dict = js2xml.make_dict(jstree.xpath('//assign[left//identifier[@name="runParams"]]/right/*')[0])

        products = self.parse_dict(dict)
        # product_id = self.items['product_id']

        self.items['products'] = products
        url = self.items['desc_url']


        # free_shipping = self.check_free_shipping(shipping_json)
        yield scrapy.Request(url=url, callback=self.parse_description)


        # yield scrapy.Request(url=url2, callback=self.get_shipping, headers = {'Accept': 'application/json',
        #                           'Referer': 'https://pl.aliexpress.com/item/32969050947.html'} )