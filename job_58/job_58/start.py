from scrapy.cmdline import execute


if __name__ == '__main__':
    # execute(["scrapy", "crawl", "xuke"])
    execute(["scrapy", "crawl", "job_58"])
    # while True:
    #
    #     # os.system('scrapy crawl fangtianxia')
    #     # os.system('scrapy crawl anjuke')
    #     try:
    #         os.system('scrapy crawl xuke')
    #         print('<<<<<<<<<<<<<<<<<<<<<<<<<<结束>>>>>>>>>>>>>>>>>>>>>>>>>')
    #         time.sleep(1)
    #
    #     except:
    #         os.system('scrapy crawl xuke')
    #         print('<<<<<<<<<<<<<<<<<<<<<<<<<<<全部结束>>>>>>>>>>>>>>>>>>>>>>>>>')
    #         time.sleep(3600)

