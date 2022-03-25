import loggig  # 引入logging模块
import os.path
import time
# 第一步，创建一个logger
logger = loggig.getLogger()
logger.setLevel(loggig.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + '/Logs/'
log_name = log_path + rq + '.log'
logfile = log_name
fh = loggig.FileHandler(logfile, mode='w')
fh.setLevel(loggig.DEBUG)  # 输出到file的log等级的开关
# 第三步，定义handler的输出格式
formatter = loggig.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)
# 日志
logger.debug('this is a logger debug message')
logger.info('this is a logger info message')
logger.warning('this is a logger warning message')
logger.error('this is a logger error message')
logger.critical('this is a logger critical message')