import os
from scrapy.cmdline import execute


if __name__ == '__main__':
    execute(["scrapy", "crawl", "detail"])
    # execute(["scrapy", "crawl", "zhaob"])
