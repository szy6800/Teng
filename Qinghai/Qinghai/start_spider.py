from scrapy.cmdline import execute
import gerapy_selenium


if __name__ == '__main__':
    execute(["scrapy", "crawl", "qh_301"])
    # execute(["scrapy", "crawl", "gs_ggzy"])
