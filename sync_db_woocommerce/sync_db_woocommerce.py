from woocommerce import API
from pymongo import MongoClient
import json
import requests
from requests import Timeout
import time
import datetime
from sympy import Symbol, Eq, solve

class SyncDbWoocommerce():

    def __init__(self, woo_category_id):
        #woocommerce category, products will be added to this category
        #TODO accept category tree instead of single category
        self.woo_category_id = woo_category_id
        #Shipping price for allegro
        self.ALLEGRO_SHIPPING_PRICE = 30
        #Markup in pln
        self.MARKUP = 15
        self.client = MongoClient()
        self.client = MongoClient('localhost', 27017)
        db = self.client['ali']
        self.collection = db['ali']
        self.wcapi = API(
            url="http://server764802.nazwa.pl/wordpress",
            consumer_key="ck_28c44a0b2526deeac2791f629e51a394f281b1ad",
            consumer_secret="cs_30e4817bbba122d6cf28c694d14f58f4c061bdbe",
            wp_api=True,
            version="wc/v3",
            timeout = 120
        )

    def clear_log(self):
        with open(r'C:\Users\donniebrasco\PycharmProjects\ali_scrapy\ali\added_products_ids.txt', 'w') as f:
            pass

    def run(self):
        # self.clear_log()
        self.check_unadded_products_in_woocommerce()

    def get_woo_id(self, response):
        return response['id']

    def check_unadded_products_in_woocommerce(self):
        unadded_products = self.collection.find({"woocommerce_id": 0})
        for product in unadded_products:
            db_id = product['_id']
            name = product['data']['product_name']
            sku = str(product['data']['product_id'])
            aliexpress_link = 'https://pl.aliexpress.com/item/{}.html'.format(sku)
            #TODO Figure out what price to put in main product
            regular_price = '15'
            description = product['data']['description']
            description_url = product['data']['desc_url']
            #TODO Create mapping between ali_categories and woo
            #categories = product['categories']
            images = product['data']['images']
            # attributes = []
            variants = self.get_all_variants_of_product(db_id)
            attributes_properties = self.get_main_product_attributes(variants)


            woo_id = self.create_main_product_woo(name, regular_price, description, attributes_properties, aliexpress_link, images, sku, description_url)

            if woo_id:
                print('Product: {} successfully added to woocommerce with id: {}'.format(aliexpress_link, woo_id))
                # self.save_added_main_product_id(woo_id)
                self.add_main_woocommerce_id_to_database(woo_id, db_id)
                self.get_all_variants_attributes(variants)
                self.create_variants_woo(woo_id, db_id, variants)

    def add_main_woocommerce_id_to_database(self, woo_id, db_id):
        self.collection.find_one_and_update({'_id': db_id}, {'$set': {'woocommerce_id': woo_id}}, upsert=True)

    def get_image_list(self, images):
        images_list = []

        for item in images:
            image = {}
            image['src'] = item
            images_list.append(image)

        return images_list

    def create_main_product_woo(self, name, regular_price, description, attributes_properties, aliexpress_link, images, sku, description_url):
        data = {}
        meta_data_list = []
        ali_url_dict = {}
        desc_url_dict = {}

        ali_url_dict['key'] = 'aliexpress_link'
        ali_url_dict['value'] = aliexpress_link
        desc_url_dict['key'] = 'aliexpress_desc_link'
        desc_url_dict['value'] = description_url

        meta_data_list.append(ali_url_dict)
        meta_data_list.append(desc_url_dict)

        data['name'] = name
        data['sku'] = sku
        data['type'] = 'variable'
        data['regular_price'] = regular_price
        data['description'] = description
        data['attributes'] = attributes_properties
        data['meta_data'] = meta_data_list
        data['images'] = self.get_image_list(images)
        #TODO figure what kind of categories we gonna use
        data['categories'] = [{'id': int(self.woo_category_id)}]
        # data['images'] = images
        response = self.wcapi.post("products", data).json()
        try:
            if response['status'] == 'publish':
                woo_id = self.get_woo_id(response)
                return woo_id
        except KeyError:
            print('Problem occurred while trying to add product: {}'.format(aliexpress_link))
            return None

    def test(self):
        pass

    def get_all_variants_of_product(self, db_id):
        item = self.collection.find_one({'_id': db_id})
        return item['data']['products']

    def get_all_variants_attributes(self, variants):
        available_attributes = {}
        colour_list = []
        size_list = []
        length_list = []
        available_attributes['colour'] = colour_list
        available_attributes['size'] = size_list
        available_attributes['length'] = length_list
        for key, val in variants.items():
            if 'colour' in val:
                colour = val['colour']
                if colour not in colour_list:
                    colour_list.append(colour)

            if 'size' in val:
                size = val['size']
                if size not in size_list:
                    size_list.append(size)

            if 'length' in val:
                length = val['length']
                if length not in length_list:
                    length_list.append(length)

        return available_attributes

    def get_variant_attributes(self, val):
        attributes = []

        if 'colour' in val:
            colour = val['colour']

            attribute = {}
            attribute['id'] = 24
            attribute['option'] = colour
            attributes.append(attribute)

        if 'size' in val:
            size = val['size']

            attribute = {}
            attribute['id'] = 6
            attribute['option'] = size
            attributes.append(attribute)

        if 'length' in val:
            length = val['length']

            attribute = {}
            attribute['id'] = 8
            attribute['option'] = length
            attributes.append(attribute)

        return attributes

    def get_usd_to_pln_rate(self):
        response = requests.get('http://api.nbp.pl/api/exchangerates/rates/A/USD/').json()
        return response['rates'][0]['mid']

    def get_pln_price(self, usd_price, usd_to_pln_rate):
        return usd_price * usd_to_pln_rate

    def get_final_aliexpress_price(self, aliexpress_price_incl_shipping):
        if aliexpress_price_incl_shipping < 12.44:
            self.ALLEGRO_SHIPPING_PRICE = 10
        allegro_price = Symbol('allegro_price')
        x = ((allegro_price - allegro_price * 0.11 + self.ALLEGRO_SHIPPING_PRICE) - aliexpress_price_incl_shipping) / 1.23
        allegro_final_price = solve(Eq(x, self.MARKUP))
        return round(allegro_final_price[0], 2)

    def set_variant_price(self, usd_price):
        usd_to_pln_rate = self.get_usd_to_pln_rate()
        pln_price = self.get_pln_price(usd_price, usd_to_pln_rate)
        return self.get_final_aliexpress_price(pln_price)

    def create_variant_dict(self, sku, variation, attributes):
        data = {}
        image = {}
        image['src'] = variation['img_url']
        #TODO Calculate regular price
        data['regular_price'] = str(self.set_variant_price(variation['price']))
        data['manage_stock'] = True
        data['stock_quantity'] = variation['qty']
        data['sku'] = sku
        data['image'] = image
        data['attributes'] = attributes

        # response = self.wcapi.post("products/{}/variations".format(woo_id), data).json()
        return data

    def add_variant_woocommerce_id_to_database(self, woo_id, db_id, sku):
        self.collection.find_one_and_update({'_id': db_id}, {'$set': {'data.products.{}.woocommerce_variant_id'.format(sku): woo_id}}, upsert=True)

    def save_added_variants_ids(self, added_variants):
        with open(r'C:\Users\donniebrasco\PycharmProjects\ali_scrapy\ali\added_products_ids.txt', 'a') as f:
            f.writelines("%s," % variant_id for variant_id in added_variants)

    def save_added_main_product_id(self, main_product_id):
        with open(r'C:\Users\donniebrasco\PycharmProjects\ali_scrapy\ali\added_products_ids.txt', 'a') as f:
            f.write("%s," % main_product_id)

    def add_variant_to_woo_batch(self, variants, woo_id):
        added_variants = []
        data = {}
        data['create'] = variants
        try:
            response = self.wcapi.post("products/{}/variations/batch".format(woo_id), data).json()
            for item in response['create']:
                variant_id = item['id']
                added_variants.append(variant_id)
            # self.save_added_variants_ids(added_variants)
            print('Variants successfully added to product_id: {}'.format(woo_id))
        except requests.exceptions.Timeout:
            print('Timeout occurred while trying to add variant to product id: {}'.format(woo_id))
            pass

    def create_variants_woo(self, woo_id, db_id, variants):
        final_variants_list = []

        for key, value in variants.items():
            #TODO ADD CREATED VARIANT ID TO DATABASE
            # self.add_variant_woocommerce_id_to_database(woo_id, db_id, key)

            if value['qty'] > 0:
                attributes = self.get_variant_attributes(value)
                data = self.create_variant_dict(key, value, attributes)
                final_variants_list.append(data)
            else:
                print('Variant: {} Can not be created due to availability on the auction (qty:{})'.format(key, value['qty']))

        if len(final_variants_list) > 100:
            raise Exception('Maximum variants for one product is 100')
        else:
            #TODO increase limition for number of variants
            self.add_variant_to_woo_batch(final_variants_list, woo_id)


    def get_main_product_attributes(self, variants):
        attributes_properties_list = []
        attributes =  self.get_all_variants_attributes(variants)
        counter = 0
        #TODO Create a function that will read avaiable attributes from woo and creat not existing
        for key, val in attributes.items():
            if val:
                if key == 'colour':
                    id = 24
                elif key == 'length':
                    id = 8
                elif key == 'size':
                    id = 6
                else:
                    raise Exception('No attributes available for {}'.format(key))

                attributes_properties_dict = {}
                attributes_properties_dict['id'] = id
                # attributes_properties_dict['name'] = name
                attributes_properties_dict['position'] = counter
                attributes_properties_dict['visible'] = True
                attributes_properties_dict['variation'] = True
                attributes_properties_dict['options'] = val
                attributes_properties_list.append(attributes_properties_dict)
                counter += 1

        return attributes_properties_list