
# -*- coding: utf-8 -*-

# @Time : 2022/4/12 15:02
# @Author : 石张毅
# @Site : 
# @File : lg.py
# @Software: PyCharm 
# -*- coding: utf-8 -*-
import logging
from flask import Flask
from logging.config import dictConfig

app = Flask(__name__)

dictConfig({
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s.%(msecs)d|%(thread)d|%(levelname)s|%(message)s'
            , 'datefmt': '%Y-%m-%d %H:%M:%S'}
        , 'detail': {
            'format': '%(asctime)s.%(msecs)d|%(thread)d|%(levelname)s|%(filename)s:%(funcName)s line %(lineno)d'
            , 'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'filters': {
    },
    'handlers': {
        'default': {
            'class': 'logging.handlers.RotatingFileHandler',  # 将日志消息发送到磁盘文件，并支持日志文件按大小切割
            'filename': '../logs/info.log',  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '../logs/error.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,  # 备份份数
            'formatter': 'detail',
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '../logs/script.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'flask': {
            'handlers': ['default', 'console', 'error'],
            'level': 'DEBUG',
            'propagate': True
        },
        'flask.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'weTest.flask': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True
        }
    }
})

logger = logging.getLogger('flask')
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    try:
        logger.info('info info')
        logger.debug('debug info')
        print(1 / 0)
    except Exception as err:
        logger.error('error message:{0}'.format(err.message), exc_info=True)  # 将异常异常信息添加到日志消息中