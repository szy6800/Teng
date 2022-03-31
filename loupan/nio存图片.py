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
file_name = "temp.png"
# file_path = "C:\\Users\\lpy\\Desktop\\{}".format(file_name)
# file_path = "E:\\TXRD_PROJECT\\PROJECT\\新建文件夹\\merge.png"
file_path = "C:\\Users\\12895\\Desktop\\temp.png"



def upload_file():
    # 创建一个客户端
    minioClient = Minio('123.126.87.126:9000',
        access_key='minioadmin',
        secret_key='minioadmin',
        secure=False
    )


    # 判断桶是否存在
    check_bucket = minioClient.bucket_exists("pictures")

    if not check_bucket:
        # 创建桶
        minioClient.make_bucket("pictures")
    try:
        logging.info("start upload file")
        # fput_object上传
        minioClient.fput_object(bucket_name="pictures", object_name="mysql/dev/{}".format(file_name),
                                file_path=file_path)
        logging.info("file {0} is successfully uploaded".format(file_name))
    except FileNotFoundError as err:
        logging.error('upload_failed: '+ str(err))
    except S3Error as err:
        logging.error("upload_failed:", err)


if __name__ == '__main__':
    upload_file()