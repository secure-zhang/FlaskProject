# -*- encoding:utf-8-*-
# 采集股原油日报所需要的所有数据
import json
from config import logger
from WindPy import *
from bs4 import BeautifulSoup
import datetime,re,pymssql,pymysql
logger = logger('YOUZHI')

class YouZhi():
    logger=logger
    def __init__(self):
        self.today = datetime.datetime.today()
        # 品种分析解析列表页面
    # wind 获取收盘价
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

    # 期货行情
    def qhhq(self,param1,param2,param3,num):
        # 分别为1 5 9 合约
        self.logger.info('正在采集期货行情...')
        data1 = self.close_api(param1,param2,num)
        data2 = self.close_api(param2,param3,num)
        data3 = self.close_api(param3,param1,num)
        data_item = {'data1':data1,'data2':data2,'data3':data3}
        return data_item

    def ypb_api(self,param1,param2,num):
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday
        wData = w.wsd('%s,%s'%(param1,param2), "close", str(lastday)[:10], str(self.today)[:10], "")
        data1 = wData.Data[0]
        data2 = wData.Data[1]
        ypb = data1[-1]/data2[-1]
        zr_ypb = data1[-2]/data2[-2]
        if ypb == zr_ypb:
            zr_ypb = data1[-3] / data2[-3]
        zd = ypb-zr_ypb
        data_item = {'ypb':'%.3f'%(ypb),'zr_ypb':'%.3f'%(zr_ypb),'zd':'%.3f'%(zd)}
        return data_item
    def ypb(self,param1,param2,param3,param4,num):
        data1 = self.ypb_api(param1,param2,num)
        data2 = self.ypb_api(param3,param4,num)
        data_item = {'data1':data1,'data2':data2}
        return data_item
    def kc_api(self,param,num):
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday
        wData = w.edb(param, str(lastday)[:10], str(self.today)[:10], "Fill=Previous")
        data = wData.Data[0]
        if len(data) < 3:
            return self.kc_api(param,num+1)
        jg = data[-1]
        zr_jg = data[-2]
        if jg == zr_jg:
            zr_jg = data[-3]
        zd = jg -zr_jg
        return {'jg':jg,'zr_jg':zr_jg,'zd':'%.2f'%zd}

    def kc(self,param1,param2,param3,):
        data1 = self.kc_api(param1,10)
        data1['jg'] = data1['jg']/10000
        data1['zr_jg'] = data1['zr_jg']/10000
        data1['zd'] = float(data1['zd']) /10000
        data2 = self.kc_api(param2,30)
        data3 = self.kc_api(param3,10)
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
        lastday = self.today - 365 * oneday
        # 历史价格
        his_wData = w.edb('%s,%s' % param, str(lastday - num * oneday)[:10], str(lastday)[:10], "Fill=Previous")
        xh_his_data = his_wData.Data[0]
        qh_his_data = his_wData.Data[1]
        xh_his_jg, xh_his_zr_jg, xh_his_zd = self.jicha(xh_his_data)
        qh_his_jg, qh_his_zr_jg, qh_his_zd = self.jicha(qh_his_data)
        his_jc = xh_his_jg - qh_his_jg

        # 今日价格
        wData = w.edb('%s,%s' % param, str(self.today - num * oneday)[:10], str(self.today)[:10], "Fill=Previous")
        data1 = wData.Data[0]
        data2 = wData.Data[1]
        xh_jg, xh_zr_jg, xh_zd = self.jicha(data1)
        qh_jg, qh_zr_jg, qh_zd = self.jicha(data2)

        jc = xh_jg - qh_jg
        zr_jc = xh_zr_jg-qh_zr_jg
        zd = jc-zr_jc
        tb_v = jc - his_jc
        tb_b = tb_v / his_jc
        data_item = {'jg': jc, 'zr_jg': zr_jc, 'zd': zd, 'tb_v': tb_v, 'tb_b': '%.2f' % tb_b}
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

    def yzlr(self, param1, param2,num):
        self.logger.info('正在采集压榨利润')
        data1 = self.kc_api(param1,num)
        data2 = self.kc_api(param2,num)
        jg = data1['jg']-data2['jg']
        zr_jg = data1['zr_jg']-data2['zr_jg']
        zd = jg-zr_jg
        data3 = {'jg':'%.2f'%jg,'zr_jg':'%.2f'%zr_jg,'zd':'%.2f'%zd}
        data_item = {'data1':data1,'data2':data2,'data3':data3}
        return data_item

    def dgcb(self, param1, param2,num):
        self.logger.info('正在采集到岗成本')
        data1 = self.kc_api(param1,num)
        data2 = self.kc_api(param2,num)
        data_item = {'data1':data1,'data2':data2}
        return data_item

    def sts(self,  param1, param2, param3,num):
        self.logger.info('正在采集升贴水')
        data1 = self.kc_api(param1,num)
        data2 = self.kc_api(param2,num)
        data3 = self.kc_api(param3,num)
        data_item = {'data1':data1,'data2':data2,'data3':data3}
        return data_item

    # wind 获取指标数据
    def sql_api(self, param):
        con = pymssql.connect(server="172.0.10.59", user="gt", password="server123!@#", database="GtData")
        cur = con.cursor()
        sql = "select  time,value from targetDatas where targetId=%s and time > '2015-01-01' order by time"
        cur.execute(sql,(param))
        result = cur.fetchall()
        cur.close()
        con.close()

        data_list = [(str(i[0]),float(i[1])) for i in result]
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
        date_list = [i[0][5:10] for i in data_16]
        data_item = {'date': date_list, 'data_list15': data_15, 'data_list16': data_16, 'data_list17': data_17,
                     'data_list18': data_18, 'data_list19': data_19}
        return data_item

    def yzlr_item(self, param1, param2):
        data1 = self.sql_api(param1)
        data2 = self.sql_api(param2)
        return {'data1':data1,'data2':data2}


    def write_mysql(self, data_items,png_items,content_items):
        con = pymysql.connect(host="94.191.80.61", user="alazhijia", password="root", db="GuanTongDaily", port=3306,
                              charset='utf8')
        cur = con.cursor()
        # 删除
        # drop_sql = 'delete from daily_shuhua where date=%s'
        # cur.execute(drop_sql,str(self.today))
        # con.commit()
        # 添加
        sql = 'insert into daily_youzhi (date,data_items,png_items,content_items) values (%s,%s,%s,%s)'
        cur.execute(sql, (str(self.today)[:10],data_items,png_items,content_items))
        con.commit()
        con.close()
        self.logger.info('油脂信息写入成功!')

    def main(self):
        w.start()
        zly_data_item = self.qhhq("P01M.DCE","P05M.DCE","P09M.DCE",5)
        dy_data_item = self.qhhq("Y01M.DCE","Y05M.DCE","Y09M.DCE",5)
        cy_data_item = self.qhhq("OI01M.CZC","OI05M.CZC","OI09M.CZC",5)
        dp_data_item = self.qhhq("M01M.DCE","M05M.DCE","M09M.DCE",5)
        cp_data_item = self.qhhq("RM01M.CZC","RM05M.CZC","RM09M.CZC",5)
        ypb_data_item = self.ypb("Y09M.DCE","M09M.DCE","OI09M.CZC","RM09M.CZC",5)
        kc_data_item = self.kc("s0117164","s5028184","s5006381")
        # # 棕榈油 豆油 豆粕 菜油 菜粕
        jc_data_item = self.jc_main(("s5006006","m0066353"),("s5005994","m0066354"),
                               ("s5006046","m0066352"),("s0142926","m0066365"),
                               ("s5005872","s0177552"),10)
        yzlr_data_item = self.yzlr("s5006006","s5006026",10)
        dgcb_data_item = self.dgcb("s0114197","s0114200",10)
        sts_data_item = self.sts("s5028913","s5028914","s5028915",10)
        yzlr_png_item = self.yzlr_item("COFEED0101266","COFEED0101271")
        data_items = {'zly_data_item':zly_data_item,'dy_data_item':dy_data_item,'cy_data_item':cy_data_item
                      ,'dp_data_item':dp_data_item,'cp_data_item':cp_data_item,'ypb_data_item':ypb_data_item
                      ,'kc_data_item':kc_data_item,'jc_data_item':jc_data_item,'yzlr_data_item':yzlr_data_item
                    ,'sts_data_item':sts_data_item,'dgcb_data_item':dgcb_data_item}
        png_items = {'yzlr_png_item':yzlr_png_item}
        data_items = json.dumps(data_items)
        png_items = json.dumps(png_items)
        content_items = json.dumps({"content_list":["略"]})
        self.write_mysql(data_items,png_items,content_items)

if __name__ == '__main__':
    yz = YouZhi()
    yz.main()