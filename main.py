from ali_scrapy.ali.run_scraper import Scraper
from pathlib import Path
import sys, os

class Main():
    def __init__(self):
        self.add_cwd_to_path()

    def add_cwd_to_path(self):
        cwd = Path.cwd()
        goal_dir = cwd / 'ali_scrapy'
        sys.path.append(str(goal_dir))

if __name__ == '__main__':
    main = Main()
    scraper = Scraper()
    scraper.run_cat_spider('200003482', 1)