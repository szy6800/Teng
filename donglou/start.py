import os
import time
from scrapy.cmdline import execute

if __name__ == '__main__':
    # execute(["scrapy", "crawl", "xinfang2"])
    execute(["scrapy", "crawl", "app"])
    # execute(["scrapy", "crawl", "xinfang"])
    # execute(["scrapy", "crawl", "xinfang2",'-o','xinfangpan.csv'])
