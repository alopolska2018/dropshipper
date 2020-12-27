from ali_scrapy.ali.run_scraper import Scraper
from scrapy_requests.scrapy_requests import ScrapyRequests
from pathlib import Path
import sys
import subprocess
import streamlit as st

class Main():
    def __init__(self):
        self.add_cwd_to_path()

    def add_cwd_to_path(self):
        cwd = Path.cwd()
        goal_dir = cwd / 'ali_scrapy'
        sys.path.append(str(goal_dir))


        #     result = name.title()
        #     st.success(result)
        # else:
        #     st.write("Press the above button..")

if __name__ == '__main__':
    test = ScrapyRequests()
    test.run_products_spider('https://pl.aliexpress.com/item/4000948921493.html', 123)
    # ali_cat = '200000669'
    # scrape_qty = 1
    # main = Main()
    # scraper = Scraper()
    # scraper.run_products_spider('1213')
    # scraper.run_cat_spider(ali_cat, scrape_qty)

    # st.title('Dropshipper')
    # st.header('Aliexpress_Scraper: ')
    # # Text Input
    # ali_cat = st.text_input("Podaj id kategorii aliexpres: ", "Pisz Tutaj...")
    # allegro_cat_id = st.text_input("Podaj id kategorii Allegro odpowiadającej tej z aliexpress: ", "Pisz Tutaj...")
    # scrape_qty = st.text_input("Podaj ilość stron do dodania(1 str to 60 produktów): ", "Pisz Tutaj...")
    # if st.button('Dodaj do sklepu'):
    #     scraper = Scraper()
    #     scraper.run_cat_spider(ali_cat, scrape_qty)
    #     # scraper.run_products_spider(allegro_cat_id)
