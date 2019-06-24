# -*- coding:utf-8 -*-
import logging
import datetime
import os



import pymysql

class SelectDatas():
    # 94.191.80.61
    # 127.0.0.1
    def select_data(self, items, db_name):
        con = pymysql.connect(host='94.191.80.61', port=3306, user='zhang', password='zhang', db='GuanTongDaily',
                              charset='utf8')
        cur = con.cursor()
        sql = "SELECT %s FROM %s ORDER BY addTime DESC LIMIT 1" % (items, db_name)
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        con.close()
        return result[0][0]

    def select_target_datas(self,tid,num):
        con = pymysql.connect(host='94.191.80.61', port=3306, user='zhang', password='zhang', db='GuanTongDaily',
                              charset='utf8')
        cur = con.cursor()
        sql = "SELECT date,value FROM target_datas where tid=%s ORDER BY date DESC LIMIT %s" % (tid,num)
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        con.close()
        return result

# 创建日志存储文件夹

def logger(logger_name):

    savepath = 'Log'
    if not os.path.exists(savepath):
        os.mkdir(r'%s' % (savepath))
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
