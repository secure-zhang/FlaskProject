# -*- encoding:utf-8-*-
# 采集尿素日报所需要的所有数据
import json
from config import logger
from WindPy import *
from bs4 import BeautifulSoup
import datetime,re,pymssql,pymysql
logger = logger('YOUZHI')


import json,os
import matplotlib as mpl
import matplotlib.pyplot as plt


plt.style.use('bmh')
# 设置中文编码和负号的正常显示
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False

class NiaoShu():
    logger=logger
    def __init__(self):
        self.today = datetime.datetime.today()

    def cyzz_api(self, param, num):
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday
        wData = w.edb(param, str(lastday)[:10], str(self.today)[:10], "Fill=Previous")
        data = wData.Data[0]
        if len(data) < 3:
            return self.cyzz_api(param,num+1)
        jg = data[-1]
        zr_jg = data[-2]
        if jg == zr_jg:
            zr_jg = data[-3]
        zd = jg -zr_jg
        return {'jg':jg,'zr_jg':zr_jg,'zd':'%.2f'%zd}

    def hca_cyzz(self,  param1, param2, param3, param4, param5, param6, param7, param8,num):
        self.logger.info('正在采集合成氨数据!')

        data1 = self.cyzz_api(param1,num)
        data2 = self.cyzz_api(param2,num)
        data3 = self.cyzz_api(param3,num)
        data4 = self.cyzz_api(param4,500)
        data5 = self.cyzz_api(param5,30)
        data6 = self.cyzz_api(param6,num)
        data7 = self.cyzz_api(param7,num)
        data8 = self.cyzz_api(param8,num)
        data_item = {'data1':data1,'data2':data2,'data3':data3,
                     'data4': data4, 'data5': data5, 'data6': data6,
                     'data7': data7, 'data8': data8}
        return data_item

    def ns_cyzz(self, param1, param2, param3, param4, param5, param6, param7, param8, num):
        self.logger.info('正在采集尿素数据!')

        data1 = self.cyzz_api(param1,num)
        data2 = self.cyzz_api(param2,num)
        data3 = self.cyzz_api(param3,num)
        data4 = self.cyzz_api(param4,num)
        data5 = self.cyzz_api(param5,num)
        data6 = self.cyzz_api(param6,num)
        data7 = self.cyzz_api(param7,300)
        data8 = self.cyzz_api(param8,num)
        data_item = {'data1':data1,'data2':data2,'data3':data3,
                     'data4': data4, 'data5': data5, 'data6': data6,
                     'data7': data7, 'data8': data8}
        return data_item
    def ls2a_cyzz(self,  param1,num):
        data1 = self.cyzz_api(param1,num)
        data_item = {'data1': data1}
        return data_item
    def dlm_cyzz(self,  param1,param2,num):
        self.logger.info('正在采集煤炭数据!')
        data1 = self.cyzz_api(param1,num)
        data2 = self.cyzz_api(param2,num)
        data_item = {'data1': data1,'data2':data2,}
        return data_item
    def ls1a_cyzz(self,  param1,param2,param3,num):
        data1 = self.cyzz_api(param1,num)
        data2 = self.cyzz_api(param2,num)
        data3 = self.cyzz_api(param3,num)
        data_item = {'data1': data1,'data2':data2,'data3':data3,}
        return data_item

    def jc_cyzz(self, param1, param2, param3, param4, param5, param6, num):
        self.logger.info('正在采集甲醇数据!')

        data1 = self.cyzz_api(param1,num)
        data2 = self.cyzz_api(param2,num)
        data3 = self.cyzz_api(param3,num)
        data4 = self.cyzz_api(param4,500)
        data5 = self.cyzz_api(param5,num)
        data6 = self.cyzz_api(param6,num)
        data_item = {'data1':data1,'data2':data2,'data3':data3,
                     'data4': data4, 'data5': data5, 'data6': data6,}
        return data_item

    def hca_png(self,param1,param2,param3, param4, param5,num):
        self.logger.info('正在采集合成氨图片数据!')
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday
        wData = w.wsd('%s,%s,%s,%s,%s'%(param1,param2,param3, param4, param5), "close",str(lastday)[:10], str(self.today)[:10], "")
        data = wData.Data
        date = wData.Times
        data_list = [(str(date[i]),data[0][i],data[1][i],data[2][i],data[3][i],data[4][i]) for i in range(len(date))]
        item = {'data1':data_list}

        return item
    def map_dap_png(self,param1,param2,param3, param4,num):
        self.logger.info('正在采集合MAP与DAP图片数据!')
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday
        wData = w.wsd('%s,%s,%s,%s'%(param1,param2,param3, param4), "close",str(lastday)[:10], str(self.today)[:10], "")
        data = wData.Data
        date = wData.Times
        data_list = [(str(date[i]),data[0][i],data[1][i],data[2][i],data[3][i]) for i in range(len(date))]
        item = {'data1':data_list}
        return item

    def five_years(self,param1):
        wData = w.edb('%s' % (param1), '2015-01-01', str(self.today)[:10], "Fill=Previous")
        date = wData.Times
        data1 = wData.Data[0]
        data_list = [(str(date[i]), data1[i]) for i in range(len(date))]

        data_15 = []
        data_16 = []
        data_17 = []
        data_18 = []
        data_19 = []

        for data in data_list:
            if data[0][2:4] == '15':
                data_15.append(data)
            if data[0][2:4] == '16':
                data_16.append(data)
            if data[0][2:4] == '17':
                data_17.append(data)
            if data[0][2:4] == '18':
                data_18.append(data)
            if data[0][2:4] == '19':
                data_19.append(data)

        date_list = [i[0][5:] for i in data_18]
        data_item = {'date': date_list, 'data_list15': data_15, 'data_list16': data_16, 'data_list17': data_17,
                     'data_list18': data_18, 'data_list19': data_19}
        return data_item
    def five_years_png(self,param1,param2,param3,param4):
        self.logger.info('正在采集五年图片数据...')
        data1 = self.five_years(param1)
        data2 = self.five_years(param2)
        data3 = self.five_years(param3)
        data4 = self.five_years(param4)
        return {'data1':data1,'data2':data2,
                'data3': data3, 'data4': data4
                }
    def write_mysql(self, data_items,png_items,content_items):
        con = pymysql.connect(host="94.191.80.61", user="alazhijia", password="root", db="GuanTongDaily", port=3306,
                              charset='utf8')
        cur = con.cursor()
        # 删除
        # drop_sql = 'delete from daily_shuhua where date=%s'
        # cur.execute(drop_sql,str(self.today))
        # con.commit()
        # 添加
        sql = 'insert into daily_niaoshu (date,data_items,png_items,content_items) values (%s,%s,%s,%s)'
        cur.execute(sql, (str(self.today)[:10],data_items,png_items,content_items))
        con.commit()
        con.close()
        self.logger.info('尿素信息写入成功!')

    def main(self):
        w.start()
        # 产业追踪
        hca_data_item = self.hca_cyzz('s5443561','s5456659','s5456660','s5456661','s5456662','s5456668','s5443563','s5456669',5)
        ns_data_item = self.ns_cyzz('s5424229','s5424228','s5424232','s5424249','s5456749','s5443659','s5456748','s5443657',5)
        ls2a_data_item = self.ls2a_cyzz('s5456673',5)
        ls1a_data_item = self.ls1a_cyzz('s5443580','s5443582','s5443583',5)
        dlm_data_item = self.dlm_cyzz('s5120090','s5120089',5)
        jc_data_item = self.jc_cyzz('s5442734','s5442739','s5442742','s5442745','s5442749','s5442754',5)
        hca_png_item = self.hca_png('s5443561','s5456659','s5456660','s5456662','s5456669',500)
        map_dap_png_item = self.map_dap_png('s5456673','s5443580','s5443582','s5443583',500)
        five_years_png_item = self.five_years_png('s5120090','s5120089','s5458274','s5471364')
        data_items = {'hca_data_item':hca_data_item,'ns_data_item':ns_data_item,'ls2a_data_item':ls2a_data_item,
                    'ls1a_data_item':ls1a_data_item,'dlm_data_item':dlm_data_item,'jc_data_item':jc_data_item,
                      }
        png_items = {'hca_png_item':hca_png_item,'map_dap_png_item':map_dap_png_item,'five_years_png_item':five_years_png_item}
        data_items = json.dumps(data_items)
        png_items = json.dumps(png_items)
        content_items = json.dumps({"content_list":["略"]})
        self.write_mysql(data_items,png_items,content_items)


if __name__ == '__main__':
    NiaoShu().main()
