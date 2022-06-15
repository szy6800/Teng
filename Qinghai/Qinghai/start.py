'''
定时采集启动程序
job
    定时器函数
    测试
BlockingScheduler
    定时器方法
'''


import os
import time
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler


def job():
    start_times = datetime.datetime.now()  # 采集开始时间
    start_time = str(start_times).split('.')[0]
    # print('starting time ===>', start_time)
    # # 采集逻辑
    # # # #
    os.system('scrapy crawl a59med')
    os.system('scrapy crawl conch')
    os.system('scrapy crawl dav')
    os.system('scrapy crawl eceg')
    os.system('scrapy crawl zgazxxw')
    # os.system('scrapy crawl postoffice')
    os.system('scrapy crawl bjmu')
    os.system('scrapy crawl bjx')
    os.system('scrapy crawl huanbao')
    os.system('scrapy crawl ggzy')
    #
    os.system('scrapy crawl hcjq')
    os.system('scrapy crawl chinabrr')
    os.system('scrapy crawl bdebid')

    os.system('scrapy crawl mof')
    os.system('scrapy crawl cdxctz')
    os.system('scrapy crawl shipoe')
    os.system('scrapy crawl dfmbidding')
    os.system('scrapy crawl fjggzyjy')
    os.system('scrapy crawl bjhd')
    os.system('scrapy crawl czzhzb')
    os.system('scrapy crawl bjchy')

    os.system('scrapy crawl ptzfcg')
    os.system('scrapy crawl miit')
    # os.system('scrapy crawl dgsy')
    os.system('scrapy crawl bzggzyjy')
    # 3/15
    os.system('scrapy crawl bankqh')
    os.system('scrapy crawl csdsj')
    os.system('scrapy crawl hhsd')
    os.system('scrapy crawl sgcc')
    os.system('scrapy crawl westmining')
    # 3/16
    os.system('scrapy crawl qhyhgf')
    os.system('scrapy crawl xntg')
    os.system('scrapy crawl tobacco')
    os.system('scrapy crawl zhengpingjituan')
    os.system('scrapy crawl icbc')
    # 3/17
    os.system('scrapy crawl ccccltd')
    os.system('scrapy crawl zmzb')
    os.system('scrapy crawl xndyyljt')
    os.system('scrapy crawl qhssyy')
    os.system('scrapy crawl qhheart')
    # 3/18
    os.system('scrapy crawl norincogroup')

    os.system('scrapy crawl gs_plsggzyjy')
    os.system('scrapy crawl gs_plsggzyjy1')
    os.system('scrapy crawl gs_gnzrmzf')
    os.system('scrapy crawl gs_gnzrmzf1')
    os.system('scrapy crawl gs_dingxi')
    os.system('scrapy crawl gs_gssey')
    os.system('scrapy crawl gs_qysggzyjy')
    os.system('scrapy crawl gs_tianshui')
    os.system('scrapy crawl gs_gsei')

    # os.system('scrapy crawl ebnew')
    print('采集已完成>>>>>>>>')

    print('collect again after 1 hour!!!!')

    end_time = str(datetime.datetime.now()).split('.')[0]  # 采集结束时间
    print(f"starting time ===> {start_time}, end time ===> {end_time}")
    next_start_time = (start_times + datetime.timedelta(days=1)).strftime('%y/%m/%d %h:%m:%s')  # 下次采集间隔时间
    print('next startup time =====>', next_start_time, '\n')


if __name__ == "__main__":
    job()
    scheduler = BlockingScheduler()  # 实例化定时器
    scheduler.add_job(job, 'cron', hour=2, minute=1)
    scheduler.add_job(job, 'cron', hour=8, minute=1)
    scheduler.add_job(job, 'cron', hour=14, minute=1)
    scheduler.add_job(job, 'cron', hour=20, minute=1)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    except SystemExit:
        print('exit')
        exit()




