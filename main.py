from scrapy_requests.scrapy_requests import ScrapyRequests
from pathlib import Path
import sys
import streamlit as st
import json

class Main():
    def __init__(self):
        self.add_cwd_to_path()

    def add_cwd_to_path(self):
        cwd = Path.cwd()
        goal_dir = cwd / 'ali_scrapy'
        sys.path.append(str(goal_dir))


    def create_list_of_urls(self, cat_spider_output):
        urls = []
        for item in cat_spider_output:
            url = item['url']
            urls.append(url)
        return urls

        #     result = name.title()
        #     st.success(result)
        # else:
        #     st.write("Press the above button..")
    def stremlit(self):
        st.title('dropshipper')

        menu = ['Moduł 1-Scraper']
        choice = st.sidebar.selectbox('Menu', menu)
        if choice == 'Moduł 1-Scraper':
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
                products_spider_output = test.run_products_spider(urls[0], allegro_cat_id)
                products_spider_output = json.loads(products_spider_output)
                if products_spider_output['status'] == 'ok':
                    st.success(f'Pobrano {str(products_spider_output["stats"]["item_scraped_count"])} produktów')
                else:
                    st.error('Wystąpił problem z pobraniem produktu')

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
