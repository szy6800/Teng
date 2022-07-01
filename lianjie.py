import datetime

start_times = datetime.datetime.now()  # 采集开始时间
print(start_times)
print(datetime.timedelta(days=1))
next_start_time = (start_times + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')  # 下次采集间隔时间
print('next startup time =====>', next_start_time, '\n')
