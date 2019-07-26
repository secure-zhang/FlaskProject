# -*- encoding:utf-8-*-
# 采集股油脂日报所需要的所有数据
import json
from config import logger
from WindPy import *
from bs4 import BeautifulSoup
import datetime,re,pymssql,pymysql
logger = logger('YUMI')

class YuMi():
    logger=logger
    def __init__(self):
        self.today = datetime.datetime.today()

    def close_api(self, param1,param2,num):
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday
        wData = w.wsd('%s,%s'%(param1,param2), "close", str(lastday)[:10], str(self.today)[:10], "")
        data1 = wData.Data[0]
        data2 = wData.Data[1]
        jg = data1[-1]-data2[-1]
        zrjg = data1[-2]-data2[-2]
        if jg == zrjg:
            zrjg = data1[-3] - data2[-3]
        zd = jg- zrjg
        return {'jg':jg,'zrjg':zrjg,'zd':zd}

    def qhhq(self,param1,param2,param3,num):
        # 分别为1 5 9 合约
        self.logger.info('正在采集期货行情...')
        data1 = self.close_api(param1,param2,num)
        data2 = self.close_api(param2,param3,num)
        data3 = self.close_api(param3,param1,num)
        data_item = {'data1':data1,'data2':data2,'data3':data3}
        return data_item
    def pzjc(self,param1,param2,param3,param4,param5,param6,num):
        self.logger.info('正在采集跨品种行情...')
        data1 = self.close_api(param1,param4,num)
        data2 = self.close_api(param2,param5,num)
        data3 = self.close_api(param3,param6,num)
        data_item = {'data1':data1,'data2':data2,'data3':data3}
        return data_item

    def jicha(self, data):
        jg = data[-1]
        zr_jg = data[-2]
        if jg == zr_jg:
            zr_jg = data[-3]
        zd = jg - zr_jg
        return jg, zr_jg, zd

    def jc(self, param, num):
        oneday = datetime.timedelta(days=1)
        wData = w.edb('%s,%s' % param, str(self.today - num * oneday)[:10], str(self.today)[:10], "Fill=Previous")
        data1 = wData.Data[0]
        data2 = wData.Data[1]
        xh_jg, xh_zr_jg, xh_zd = self.jicha(data1)
        qh_jg, qh_zr_jg, qh_zd = self.jicha(data2)
        jc = xh_jg - qh_jg
        zr_jc = xh_zr_jg-qh_zr_jg
        zd = jc-zr_jc
        data_item = {'jg': jc, 'zr_jg': zr_jc, 'zd': zd}
        return data_item

    def jc_main(self, param1, param2, param3, param4, param5, num):
        self.logger.info('正在采集基差')
        data1 = self.jc(param1, num)
        data2 = self.jc(param2, num)
        data3 = self.jc(param3, num)
        data4 = self.jc(param4, num)
        data5 = self.jc(param5, num)
        data_item = {'data1': data1, 'data2': data2, 'data3': data3, 'data4': data4, 'data5': data5}
        return data_item

    def dfxh_main(self, param1, param2, param3,num):
        self.logger.info('正在采集基差')
        data1 = self.jklr_(param1, num)
        data2 = self.jklr_(param2, num)
        data3 = self.jklr_(param3, num)
        data_item = {'data1': data1, 'data2': data2, 'data3': data3}
        return data_item
    def jklr_(self, param, num):
        oneday = datetime.timedelta(days=1)
        wData = w.edb('%s' % param, str(self.today - num * oneday)[:10], str(self.today)[:10], "Fill=Previous")
        data = wData.Data[0]
        jg = data[-1]
        zr_jg = data[-2]
        if jg == zr_jg:
            zr_jg = data[-3]
        zd = jg - zr_jg
        data_item = {'jg': jg, 'zr_jg': zr_jg, 'zd': float('%.2f'%zd)}
        return data_item
    def jklr_main(self, param1, param2,num):
        data1 = self.jklr_(param1,num)
        data2 = self.jklr_(param2,num)
        data3 = {'jg':float('%.2f'%(data1['jg']-data2['jg'])) , 'zr_jg': float('%.2f'%(data1['zr_jg']-data2['zr_jg'])) , 'zd': data1['zd']-data2['zd']}
        data_item = {'data1': data1, 'data2': data2, 'data3': data3}
        return data_item
    def xhjg_main(self,param1):
        self.logger.info('正在采集现货库存...')
        wData = w.edb('%s'%(param1), '2017-01-01', str(self.today)[:10], "Fill=Previous")
        date = wData.Times
        data1 = wData.Data[0]
        data_list = [(str(date[i]),data1[i]) for i in range(len(date))]

        data_17 = []
        data_18 = []
        data_19 = []

        for data in data_list:
            if data[0][2:4] == '17':
                data_17.append(data)
            if data[0][2:4] == '18':
                data_18.append(data)
            if data[0][2:4] == '19':
                data_19.append(data)
        date_list = [i[0][5:] for i in data_18]
        data_item = {'date':date_list,'data_list17':data_17,'data_list18':data_18,'data_list19':data_19}
        return data_item

    def sdwf_main(self,param1):
        self.logger.info('正在采集山东潍坊...')
        wData = w.edb('%s'%(param1), '2017-01-01', str(self.today)[:10], "Fill=Previous")
        date = wData.Times
        data1 = wData.Data[0]
        data_list = [(str(date[i]),data1[i]) for i in range(len(date))]

        data_17 = []
        data_18 = []
        data_19 = []

        for data in data_list:
            if data[0][2:4] == '17':
                data_17.append(data)
            if data[0][2:4] == '18':
                data_18.append(data)
            if data[0][2:4] == '19':
                data_19.append(data)
        date_list = [i[0][5:] for i in data_17]
        data_item = {'date':date_list,'data_list17':data_17,'data_list18':data_18,'data_list19':data_19}
        return data_item
    def sql_api(self, param):
        self.logger.info('正在采集玉米库存...')
        con = pymssql.connect(server="172.0.10.59", user="gt", password="server123!@#", database="GtData")
        cur = con.cursor()
        sql = "select  time,value from targetDatas where targetId=%s and time > '2017-01-01' order by time"
        cur.execute(sql,(param))
        result = cur.fetchall()
        cur.close()
        con.close()

        data_list = [(str(i[0]),float(i[1])) for i in result]
        data_17 = []
        data_18 = []
        data_19 = []

        for data in data_list:
            if data[0][2:4] == '17':
                data_17.append(data)
            if data[0][2:4] == '18':
                data_18.append(data)
            if data[0][2:4] == '19':
                data_19.append(data)

        date_list = [i[0][5:10] for i in data_18]
        data_item = {'date': date_list, 'data_list17': data_17,
                     'data_list18': data_18, 'data_list19': data_19}
        return data_item
    def jklr_png_main(self,param1,param2):
        self.logger.info('正在采集进口利润...')
        wData = w.edb('%s,%s'%(param1,param2), '2017-01-01', str(self.today)[:10], "Fill=Previous")
        date = wData.Times
        data1 = wData.Data[0]
        data2 = wData.Data[1]
        data_list = [(str(date[i]),data1[i]-data2[i]) for i in range(len(date))]

        data_17 = []
        data_18 = []
        data_19 = []

        for data in data_list:
            if data[0][2:4] == '17':
                data_17.append(data)
            if data[0][2:4] == '18':
                data_18.append(data)
            if data[0][2:4] == '19':
                data_19.append(data)
        date_list = [i[0][5:] for i in data_17]
        data_item = {'date':date_list,'data_list17':data_17,'data_list18':data_18,'data_list19':data_19}
        return data_item
    def write_mysql(self, data_items,png_items,content_items):
        con = pymysql.connect(host="94.191.80.61", user="alazhijia", password="root", db="GuanTongDaily", port=3306,
                              charset='utf8')
        cur = con.cursor()
        # 删除
        # drop_sql = 'delete from daily_shuhua where date=%s'
        # cur.execute(drop_sql,str(self.today))
        # con.commit()
        # 添加
        sql = 'insert into daily_yumi (date,data_items,png_items,content_items) values (%s,%s,%s,%s)'
        cur.execute(sql, (str(self.today)[:10],data_items,png_items,content_items))
        con.commit()
        con.close()
        self.logger.info('玉米信息写入成功!')

    def main(self):
        w.start()
        ym_data_item = self.qhhq("C01M.DCE","C05M.DCE","C09M.DCE",5)
        df_data_item = self.qhhq("CS01M.DCE","CS05M.DCE","CS09M.DCE",5)
        kpz_data_item = self.pzjc("C01M.DCE","C05M.DCE","C09M.DCE","CS01M.DCE","CS05M.DCE","CS09M.DCE",5)
        jc_data_item = self.jc_main(("s5005771","m0066350"),("s5005775","m0066350"),
                               ("s5005778","m0066350"),("s5005784","m0066350"),
                               ("s5005789","m0066350"),10)
        dfxh_data_item = self.dfxh_main('s5006501','s5006504','s5006505',10)
        jckr_data_item = self.jklr_main('s5005793','s5005808',10)
        xhjg_png_item = self.xhjg_main('s5005789')
        ymkc_png_item = self.sql_api('COFEED0103844')
        jckr_png_item = self.jklr_png_main('s5005793','s5005808')
        sdwf_png_item = self.sdwf_main('s5006505')
        data_items = {'dfxh_data_item':dfxh_data_item,'ym_data_item':ym_data_item,'df_data_item':df_data_item,'kpz_data_item':kpz_data_item,
                      'jc_data_item':jc_data_item,'jckr_data_item':jckr_data_item}
        png_items = {'xhjg_png_item':xhjg_png_item,'ymkc_png_item':ymkc_png_item,'jckr_png_item':jckr_png_item,'sdwf_png_item':sdwf_png_item}
        data_items = json.dumps(data_items)
        png_items = json.dumps(png_items)
        content_items = json.dumps({"content_list":["略"]})
        self.write_mysql(data_items,png_items,content_items)









if __name__ == '__main__':
    YuMi().main()
