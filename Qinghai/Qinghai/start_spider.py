from scrapy.cmdline import execute
import gerapy_selenium

if __name__ == '__main__':
    execute(["scrapy", "crawl", "test"])
    # execute(["scrapy", "crawl", "qhrch",'-o','a.csv'])


