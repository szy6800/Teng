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

    os.system('scrapy crawl fzgg')
    os.system('scrapy crawl cinn')
    os.system('scrapy crawl gssgxy')
    os.system('scrapy crawl gxj')
    os.system('scrapy crawl china_aii')
    os.system('scrapy crawl nea')

    print('采集已完成>>>>>>>>')
    print('collect again after 1 hour!!!!')
    end_time = str(datetime.datetime.now()).split('.')[0]  # 采集结束时间
    print(f"starting time ===> {start_time}, end time ===> {end_time}")
    next_start_time = (start_times + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')  # 下次采集间隔时间
    print('next startup time =====>', next_start_time, '\n')


if __name__ == "__main__":
    job()
    scheduler = BlockingScheduler()  # 实例化定时器
    scheduler.add_job(job, 'cron', hour=10, minute=4)
    scheduler.add_job(job, 'cron', hour=16, minute=2)
    scheduler.add_job(job, 'cron', hour=22, minute=2)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    except SystemExit:
        print('exit')
        exit()




