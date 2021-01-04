from scrapy_requests.scrapy_requests import ScrapyRequests
from sync_db_woocommerce.sync_db_woocommerce import SyncDbWoocommerce
from pathlib import Path
import sys
import streamlit as st
import json
from pymongo import MongoClient

class Main():
    def __init__(self):
        self.add_cwd_to_path()
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['ali']
        self.collection = self.db['ali']
        self.config = self.open_config_json()


    def open_config_json(self):
        with open('config.json') as config_file:
            config = json.load(config_file)
            return config

    def add_cwd_to_path(self):
        cwd = Path.cwd()
        goal_dir = cwd / 'ali_scrapy'
        sys.path.append(str(goal_dir))

    def check_products_in_db(self, id):
        result = self.collection.count_documents({"_id":id}) > 0
        return result

    #In order to check if product is successfully added to db
    # we need to create a list of id's and check existence of each in db
    def create_product_list_added_to_db(self, urls):
        product_list = []
        for url in urls:
            product_id = self.extract_product_id_from_url(url)
            product_list.append(product_id)
        return product_list

    def check_if_successfully_added(self, product_list):
        success = []
        failure = []
        for id in product_list:
            id_exist = self.check_products_in_db(int(id))
            if id_exist:
                success.append(id)
            else:
                failure.append(id)
        self.print_products_spider_outcome(success, failure)

    def print_products_spider_outcome(self, sucess, failure):
        st.markdown('**Numery Id poprawnie dodane do bazy:**')
        st.write(sucess)
        st.markdown('Numery Id nie dodane do bazy:')
        st.write(failure)


    def create_list_of_urls(self, cat_spider_output):
        urls = []
        for item in cat_spider_output:
            url = item['url']
            urls.append(url)
        return urls

    def extract_product_id_from_url(self, url):
        url = url.split('/')
        url = url[4]
        return url[:-5]

    def streamlit_module_scraper(self):
        st.subheader('Moduł 1-Scraper')
        # Text Input
        ali_cat = st.text_input("Podaj id kategorii aliexpres: ", "200190013")
        allegro_cat_id = st.text_input("Podaj id kategorii Allegro odpowiadającej tej z aliexpress: ", "1")
        pages = st.text_input("Podaj ilość stron do dodania(1 str to 60 produktów): ", "1")
        if st.button('Dodaj do sklepu'):
            test = ScrapyRequests()
            cat_spider_output = test.run_cat_spider_get(ali_cat, pages)
            cat_spider_output = json.loads(cat_spider_output)
            if cat_spider_output['status'] == 'ok':
                st.success(f'Pobrano {str(cat_spider_output["stats"]["item_scraped_count"])} url dla kategorii')
                st.write(cat_spider_output['items'])
            else:
                st.error('Wystąpił problem z pobraniem url dla kategorii')
                # st.json(cat_spider_output['items'])

            urls = self.create_list_of_urls(cat_spider_output['items'])
            products_spider_output = test.run_products_spider_post(urls, allegro_cat_id)
            products_spider_output = json.loads(products_spider_output)
            if products_spider_output['status'] == 'ok':
                st.success(f'Pobrano {str(products_spider_output["stats"]["item_scraped_count"])} produktów')
                product_list = self.create_product_list_added_to_db(urls)
                self.check_if_successfully_added(product_list)
            else:
                st.error('Wystąpił problem z pobraniem produktu')

    def streamlit_module_woocommerce(self):
        st.subheader('Moduł 2-Dodawanie_do_woocommerce')
        woo_category_id = st.text_input("Podaj id kategorii woocommerce do której dodam produkty: ", "2015")
        woocommerce_db_sync = SyncDbWoocommerce(woo_category_id)
        if st.button('Dodaj do woocommerce'):
            woocommerce_db_sync.run()

    def open_removebg_accounts_file(self):
        with open('removebg_accounts.json', 'r') as file:
            accounts_dict = json.load(file)
            return accounts_dict

    def streamlit_module_removebg(self):
        st.subheader('Moduł 3-Removebg')
        remove_bg_accounts = self.open_removebg_accounts_file()
        if st.button('Wyświetl listę kont removebg'):
            st.write(remove_bg_accounts)


        # index = 0
        # accounts_dict = self.open_json_file()
        # for account in accounts_dict['accounts']:
        #     if 'api_key' in account:
        #         index += 1
        #     else:
        #         st.write(account["login"])
        #         st.write(account["password"])
        #         api_key = st.text_input('Podaj api_key', '213', key=index)
        #         print(f'login: {account["login"]}, password: {account["password"]}')
        #         # api_key = input('Podaj klucz api: ')
        #         # if st.button('Dodaj'):
        #         accounts_dict['accounts'][index]['api_key'] = api_key
        #         index += 1
        # print(accounts_dict)


    def stremlit(self):
        st.title('dropshipper')
        menu = ['Moduł 1-Scraper', 'Moduł 2-Dodawanie_do_woocommerce', 'Moduł 3-Removebg']
        choice = st.sidebar.selectbox('Menu', menu)
        if choice == 'Moduł 1-Scraper':
           self.streamlit_module_scraper()
        elif choice == 'Moduł 2-Dodawanie_do_woocommerce':
            self.streamlit_module_woocommerce()
        elif choice == 'Moduł 3-Removebg':
            self.streamlit_module_removebg()

if __name__ == '__main__':
    test = Main()
    test.stremlit()




    # # test.run_products_spider('https://pl.aliexpress.com/item/4000948921493.html', 123)
    # # ali_cat = '200000669'
    # # scrape_qty = 1
    # # main = Main()
    # # scraper = Scraper()
    # # scraper.run_products_spider('1213')
    # # scraper.run_cat_spider(ali_cat, scrape_qty)
    #
    # st.title('Dropshipper')
    # st.header('Aliexpress_Scraper: ')
    # Text Input
    # ali_cat = st.text_input("Podaj id kategorii aliexpres: ", "Pisz Tutaj...")
    # allegro_cat_id = st.text_input("Podaj id kategorii Allegro odpowiadającej tej z aliexpress: ", "Pisz Tutaj...")
    # pages = st.text_input("Podaj ilość stron do dodania(1 str to 60 produktów): ", "Pisz Tutaj...")
    # if st.button('Dodaj do sklepu'):
    #     test = ScrapyRequests()
    #     cat_spider_output = test.run_cat_spider_get(ali_cat, pages)
    #     if cat_spider_output['status'] == 'ok':
    #
    #     # scraper.run_products_spider(allegro_cat_id)
