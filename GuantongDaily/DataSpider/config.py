# -*- coding:utf-8 -*-
import logging
import datetime
import os

# 创建日志存储文件夹
def mkdir():
    pwd = os.path.dirname(__file__)
    dir_name = 'Log'
    savepath = r'%s\%s' % (pwd, dir_name)
    if not os.path.exists(savepath):
        os.mkdir(r'%s' % (savepath))
    return savepath

def logger(logger_name):
    savepath = mkdir()

    # 在控制台输出
    logger = logging.getLogger(logger_name)
    logger.setLevel(level=logging.DEBUG)

    today = datetime.datetime.today()
    y, m, d = str(today).split()[0].split('-')

    # 将级别大于error的日志记录到文件中
    handler = logging.FileHandler(
        filename='%s\log_%s_%s_%s.log' % (savepath, y[2:], m, d))
    handler.setLevel(level=logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # 输出到控制台
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
