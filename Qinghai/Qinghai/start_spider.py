from scrapy.cmdline import execute
import gerapy_selenium

if __name__ == '__main__':
    execute(["scrapy", "crawl", "gs_cai"])
    # execute(["scrapy", "crawl", "qhrch",'-o','a.csv'])


