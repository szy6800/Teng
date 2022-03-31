# -*- coding: utf-8 -*-

# @Time : 2022/3/10 18:16
# @Author : 石张毅
# @Site : 
# @File : scf.py
# @Software: PyCharm

import logging
from minio import Minio
from minio.error import S3Error

logging.basicConfig(
    level=logging.INFO,
    filename='../mysqlbackup_up.log',
    filemode='a',
    format='%(asctime)s %(name)s %(levelname)s--%(message)s'
)

# 确定要上传的文件
file_name = "*****"
file_path = "C:\\Users\\lpy\\Desktop\\{}".format(file_name)


def upload_file():
    # 创建一个客户端
    minioClient = Minio(
        'minio.***.com',
        access_key='admin',
        secret_key='****',
        secure=False
    )

    # 判断桶是否存在
    check_bucket = minioClient.bucket_exists("backup")

    if not check_bucket:
        minioClient.make_bucket("backup")
    try:
        logging.info("start upload file")
        minioClient.fput_object(bucket_name="backup", object_name="mysql/dev/{}".format(file_name),
                                file_path=file_path)
        logging.info("file {0} is successfully uploaded".format(file_name))
    except FileNotFoundError as err:
        logging.error('upload_failed: '+ str(err))
    except S3Error as err:
        logging.error("upload_failed:", err)


if __name__ == '__main__':
    upload_file()