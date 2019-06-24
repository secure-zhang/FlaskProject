
from WindPy import *
import pymssql

import datetime
import time
import queue
import logging
import threading
lock = threading.RLock()
# 在控制台输出
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

# 将级别大于error的日志记录到文件中
handler = logging.FileHandler(filename='windTarget.log')
handler.setLevel(level=logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 输出到控制台
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class WindApi:
    def __init__(self):
        self.startTime = ''
        self.con = pymssql.connect(
            server="172.0.10.59",
            user="gt",
            password="server123!@#",
            database="GtData")
        self.tid_queue=queue.Queue()
        self.data_queue = queue.Queue()

    def _readTxt(self):
        '''读取文件获得指标信息'''
        with open('jbm.txt', 'r', encoding='utf-8') as f:
            file = f.read()
        for i in file.split('\n'):
            if not i :
                continue
            list1 = i.split()
            tid = list1[0].strip()
            # print(tid)
            self.tid_queue.put(tid)
    def write_Datas(self, tid,date,value):
        '''写入指标数据'''
        cur = self.con.cursor()
        lock.acquire()

        select_sql = 'select * from TargetDatas where TargetId=%s and Time=%s'
        cur.execute(select_sql, (tid, date))
        result = cur.fetchall()
        if result:
            lock.release()
            logger.info('%s %s Datas existence' % (tid, date))
            return
        try:
            nowTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            insertsql = 'insert into TargetDatas (TargetId,Value,Time,UpdateTime,Modified,AddTime) values (%s,%s,%s,%s,%s,%s)'
            cur.execute(insertsql, (tid, value, date, date, 0, nowTime))
            self.con.commit()
            logger.info('%s %s Datas Success +1' % (tid, date))
        except:
            logger.error('sql server write error ! Date:[%s]'%(date))
        finally:
            lock.release()


    def write_error_bname(self,tid):
        '''记录采集失败'''
        with open('ErrorTid','a',encoding='utf-8') as f:
            f.write('%s\n'%tid)

    def dataItem(self,tid,start_time):
        '''指标数据'''
        today = datetime.date.today()
        wdata = w.edb(u"%s" % tid, start_time, str(today))
        if 'CWSDService' in str(wdata):
            self.write_error_bname(tid)
            return
        date = wdata.Times
        data = wdata.Data[0]
        item = dict(zip(date,data))
        return item


    def main(self):
        w.start(waitTime=60)
        self._readTxt()
        while not self.tid_queue.empty():
            tid = self.tid_queue.get()

            if not tid:
                continue
            start_time = '2010-01-01'
            # start_time = ''
            item = self.dataItem(tid,start_time)     # 指标数据
            # print(item)
            if item is None:
                continue
            [self.data_queue.put((tid,k, v)) for k, v in item.items()]
            threads = []
            thread_count = 32
            for i in range(thread_count):
                threads.append(Threads(self.data_queue,self.write_Datas))
            for i in threads:
                i.start()
            for i in threads:
                i.join()
#
        self.con.close()
#
class Threads(threading.Thread):
    def __init__(self,data_queue, write_Datas):
        threading.Thread.__init__(self)
        self.data_queue = data_queue
        self.write_Datas = write_Datas

    def run(self):
        while not self.data_queue.empty():
            data = self.data_queue.get()
            tid = data[0]
            date = data[1]
            value = data[2]
            self.write_Datas(tid,date,value)


if __name__ == '__main__':
    '''抓取历史指标数据'''
    wa = WindApi()
    wa.main()
