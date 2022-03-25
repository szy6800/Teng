import os
import time


if __name__ == '__main__':
    while True:

        # os.system('scrapy crawl fangtianxia')
        # os.system('scrapy crawl anjuke')
        try:
            os.system('scrapy crawl xinfang')
            print('<<<<<<<<<<<<<<<<<<<<<<<<<<结束>>>>>>>>>>>>>>>>>>>>>>>>>')
            time.sleep(60)

        except:
            os.system('scrapy crawl xinfang')
            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<全部结束>>>>>>>>>>>>>>>>>>>>>>>>>')
            time.sleep(60)