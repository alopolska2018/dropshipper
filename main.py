from ali_scrapy.ali.run_scraper import Scraper
from pathlib import Path
import sys
import streamlit as st

class Main():
    def __init__(self):
        self.add_cwd_to_path()

    def add_cwd_to_path(self):
        cwd = Path.cwd()
        goal_dir = cwd / 'ali_scrapy'
        sys.path.append(str(goal_dir))

    def run(self):
        st.title('Dropshipper')
        st.header('Aliexpress_Scraper: ')

        # Text Input
        ali_cat = st.text_input("Podaj id kategorii aliexpres: ", "Pisz Tutaj...")
        allegro_cat = st.text_input("Podaj id kategorii Allegro odpowiadającej tej z aliexpress: ", "Pisz Tutaj...")
        scrape_qty = st.text_input("Podaj ilość przedmiotów, które mają zostać dodane do sklepu: ", "Pisz Tutaj...")
        if st.button('Dodaj do sklepu'):
            scraper = Scraper()
            scraper.run_cat_spider('200003482', 1)


        #     result = name.title()
        #     st.success(result)
        # else:
        #     st.write("Press the above button..")

if __name__ == '__main__':
    main = Main()
    main.run()
