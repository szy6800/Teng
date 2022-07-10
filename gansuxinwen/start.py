'''
定时采集启动程序
job
    定时器函数
BlockingScheduler
    定时器方法
'''

import os
import time
if __name__ == '__main__':
    # while True:
    os.system('scrapy crawl fzgg')
    # os.system('scrapy crawl qhggzyjy')




# import datetime
# import os
# import time
# from apscheduler.schedulers.blocking import BlockingScheduler
#
# def job():
#     start_times = datetime.datetime.now()  # 采集开始时间
#     start_time = str(start_times).split('.')[0]
#     print('本次启动时间', start_time)
#
#     # 采集逻辑
#     print('正在抓取=======>招标网站!!!!<=======')
#     # os.system('scrapy crawl zbwmy')
#     time.sleep(10)
#     print('1天 后重新采集')
#
#     end_time = str(datetime.datetime.now()).split('.')[0]  # 采集结束时间
#     print(f"本次启动时间: {start_time}, 本次结束时间: {end_time}")
#     next_start_time = (start_times + datetime.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')  # 下次采集间隔时间
#     print('下次启动时间', next_start_time)
#
# if __name__ == "__main__":
#     scheduler = BlockingScheduler()  # 实例化定时器
#     scheduler.add_job(job, 'cron', hour=1, minute=1)
#     scheduler.add_job(job, 'cron', hour=2, minute=1)
#     scheduler.add_job(job, 'cron', hour=3, minute=1)
#     scheduler.add_job(job, 'cron', hour=4, minute=1)
#     scheduler.add_job(job, 'cron', hour=5, minute=1)
#     scheduler.add_job(job, 'cron', hour=6, minute=1)
#     scheduler.add_job(job, 'cron', hour=7, minute=1)
#     scheduler.add_job(job, 'cron', hour=8, minute=1)
#     scheduler.add_job(job, 'cron', hour=9, minute=1)
#     scheduler.add_job(job, 'cron', hour=10, minute=1)
#     scheduler.add_job(job, 'cron', hour=11, minute=1)
#     scheduler.add_job(job, 'cron', hour=12, minute=1)
#     try:
#         scheduler.start()
#     except (KeyboardInterrupt, SystemExit):
#         pass
#     except SystemExit:
#         print('exit')
#         exit()





