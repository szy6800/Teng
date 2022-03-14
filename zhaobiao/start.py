'''
定时采集启动程序
job
    定时器函数
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
    print('Starting time ===>', start_time)

    # 采集逻辑
    # # os.system('scrapy crawl fsggzy')
    os.system('scrapy crawl ccgp_qh')
    os.system('scrapy crawl qhcxzb')
    os.system('scrapy crawl qhei')
    os.system('scrapy crawl qhggzyjy')
    os.system('scrapy crawl ccgpgov')
    os.system('scrapy crawl mofgov')
    os.system('scrapy crawl weain')

    print('采集已完成>>>>>>>>')

    print('Collect again after 1 hour!!!!')

    end_time = str(datetime.datetime.now()).split('.')[0]  # 采集结束时间
    print(f"Starting time ===> {start_time}, End time ===> {end_time}")
    next_start_time = (start_times + datetime.timedelta(days=1)).strftime('%Y/%m/%d %H:%M:%S')  # 下次采集间隔时间
    print('Next startup time =====>', next_start_time, '\n')


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





