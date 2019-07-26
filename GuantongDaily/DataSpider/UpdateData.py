# 获取数据
import os

from WindPy import *
import pymysql
import datetime
import time
import queue
import threading
lock = threading.RLock()
import logging

# 在控制台输出
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

# 将级别大于error的日志记录到文件中
handler = logging.FileHandler(filename='WindSpider.log')
handler.setLevel(level=logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 输出到控制台
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

class ThreadsWriteData(threading.Thread):
    def __init__(self,data_queue, write_sql):
        threading.Thread.__init__(self)
        self.data_queue = data_queue
        self.write_sql = write_sql

    def run(self):
            while not self.data_queue.empty():
                tid, date, data = self.data_queue.get()
                self.write_sql(tid, date,data)

class ThreadsGetTargetid(threading.Thread):
    def __init__(self,targetid_queue, get_end_time_date):
        threading.Thread.__init__(self)
        self.targetid_queue = targetid_queue
        self.get_end_time_date = get_end_time_date

    def run(self):
        while not self.targetid_queue.empty():
            while not self.targetid_queue.empty():
                tid = self.targetid_queue.get()
                self.get_end_time_date(tid)


class WindSpider:
    def __init__(self):
        self.targetid_queue = queue.Queue()
        self.error_tid_queue = queue.Queue()
        self.targetid_end_time_queue = queue.Queue()
        self.today = datetime.date.today()
        self.oneday = datetime.timedelta(days=1)
        self.data_queue = queue.Queue()
        self.con = pymysql.connect(host="94.191.80.61", user="alazhijia", password="root", db="GuanTongDaily",
                                   port=3306,
                                   charset='utf8')
        self.kg = 0 # 开关
        self.start_time = '2010-04-16'


    # 从文件中获取需要采集的wind指标ID,以及需要采集的时间
    def get_targetid(self):
        with open('jbm.txt','r',encoding='utf-8') as f:
            lines_list = f.readlines()
        [self.targetid_queue.put(tid.strip().split(',')[0])for tid in lines_list if tid]


        threads = []
        thread_count = 32
        for i in range(thread_count):
            threads.append(ThreadsGetTargetid(self.targetid_queue, self.get_end_time_date))
        for i in threads:
            i.start()
        for i in threads:
            i.join()

    # 从数据中中获取该指标的最后更新日期
    def get_end_time_date(self, tid):
        lock.acquire()
        try:
            sql = 'SELECT  DATE FROM target_datas WHERE tid=%s ORDER BY DATE DESC LIMIT 1'
            cur = self.con.cursor()
            cur.execute(sql,tid)
            result = cur.fetchall()
            if  result:
                end_time = str(result[0][0])[:10]
            else:
                end_time = '2010-01-01'
            cur.close()
            logger.info('TID: %s 最后更新时间: %s'%(tid,end_time))
            item = {'tid':tid,'end_time':end_time}
            self.targetid_end_time_queue.put(item)
        except:
            logger.error('Error : get_end_time_date'%())
        finally:
            lock.release()

    # 记录wind采集失败指标
    def write_error_tid(self):
        if os.path.exists('error_tid.txt'):
            os.remove('error_tid.txt')
        while not self.error_tid_queue.empty():
            with open('error_tid.txt','a',encoding='utf-8') as f:
                f.write('%s\n'%self.error_tid_queue.get())

    # 从wind中获取待采集指标的数据
    def get_datas(self,tid,start_time):
        wdata = w.edb(u"%s" % tid, start_time, str(self.today))
        if 'CWSDService' in str(wdata):
            self.error_tid_queue.put(tid)
            logger.error('%s %s 数据获取失败'%(tid,start_time))
            return
        date = wdata.Times[1:]
        data = wdata.Data[0][1:]
        item = dict(zip(date,data))
        return item
    def get_datas2(self,tid,start_time):
        wdata = w.wsd('%s' % (tid), "close", start_time,str(self.today), "")
        if 'CWSDService' in str(wdata):
            self.error_tid_queue.put(tid)
            logger.error('%s %s 数据获取失败'%(tid,start_time))
            return
        date = wdata.Times[1:]
        data = wdata.Data[0][1:]
        item = dict(zip(date,data))
        return item

    def write_Datas(self, tid,date,value):
        '''写入指标数据'''
        cur = self.con.cursor()
        lock.acquire()

        select_sql = 'select * from target_datas where tid=%s and date=%s'
        cur.execute(select_sql, (tid, date))
        result = cur.fetchall()
        if result:
            lock.release()
            logger.info('%s %s Datas existence' % (tid, date))
            return
        try:
            insertsql = 'insert into target_datas (tid,value,date) values (%s,%s,%s)'
            cur.execute(insertsql, (tid, value, date))
            self.con.commit()

            logger.info('%s %s Datas Success +1' % (tid, date))
        except:
            logger.error('sql server write error ! Date:[%s]'%(date))
        finally:
            cur.close()
            lock.release()

    def run(self):
        w.start()
        self.get_targetid()
        while not self.targetid_end_time_queue.empty():
            time_start = time.time()
            targetid = self.targetid_end_time_queue.get()
            tid = targetid['tid']
            start_time = targetid['end_time']

            # 开关 控制待指标的采集开始时间
            if self.kg:
                start_time = self.start_time

            # 从wind api 中获取数据
            if '.DCE' in tid:
                item = self.get_datas2(tid,start_time)
            else:
                item = self.get_datas(tid,start_time)
            if not item: continue
            item = [self.data_queue.put((tid,str(date),data)) for date, data in item.items() if date and data]

            # 多线程写入
            threads = []
            thread_count = 32
            for i in range(thread_count):
                threads.append(ThreadsWriteData(self.data_queue,self.write_Datas))
            for i in threads:
                i.start()
            for i in threads:
                i.join()

            logger.info('TID: %s 写入: %s条 用时: %s'%(tid,len(item),time.time()-time_start))
        self.write_error_tid()


if __name__ == '__main__':
    WindSpider().run()