# -*- encoding:utf-8-*-
# 采集股指日报所需要的所有数据
import json
from config import logger
from WindPy import *
from bs4 import BeautifulSoup
import requests,datetime,re,pymssql,pymysql
logger = logger('GUZHI')

class GuZhi():
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0',
               'Host':'www.99qh.com'}
    logger=logger
    def __init__(self):
        self.today = datetime.datetime.today()-datetime.timedelta(days=1)

    # wind 获取收盘价
    def close_api(self, param,num):
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday

        wData = w.wsd(param, "pre_close,close,chg,pct_chg,amt", str(lastday)[:10], str(self.today)[:10], "")
        data = wData.Data
        return {'jg':data[1][-1],'zrjg':data[0][-1],'zd':'%.2f'%data[2][-1] ,'zdf':'%.2f'%data[3][-1],'cje':'%.2f'%(data[4][-1]/10000)}

    # 期货行情
    def qhhq(self,param1,param2,param3,num):
        self.logger.info('正在采集期货行情...')
        data1 = self.close_api(param1,num)
        data2 = self.close_api(param2,num)
        data3 = self.close_api(param3,num)
        data_item = {'data1':data1,'data2':data2,'data3':data3}
        return data_item



    def parse_html(self,url,day):
        html = self.get_html(url,day)
        soup = BeautifulSoup(html, 'lxml').p.text.strip()
        soup = soup.split('持卖单量排名')
        item = {'dc': 0, 'dc_zj': 0, 'kc': 0, 'kc_zj': 0, 'jkd': 0}
        for td in soup[1].split('\n')[2:]:
            td_list = td.replace(' ', '').split(',')
            item['dc'] += int(td_list[7])
            item['dc_zj'] += int(td_list[8])
            item['kc'] += int(td_list[10])
            item['kc_zj'] += int(td_list[11])
            item['jkd'] += (int(td_list[10]) - int(td_list[7]))
        return item

    def get_html(self,url,day):
        day = day.replace('-', '')
        url = 'http://www.cffex.com.cn/sj/ccpm/%s/%s/%s.csv' % (day[0:6], day[-2:], url)
        html = requests.get(url=url,headers=self.header)
        if html.status_code == 200:
            return html.content.decode('GBK')

    def jkcc(self):
        self.logger.info('正在采集净空持仓...')
        data1 = self.parse_html('IF_1',str(self.today)[:10])
        data2 = self.parse_html('IH_1',str(self.today)[:10])
        data3 = self.parse_html('IC_1',str(self.today)[:10])
        data4 = {'dc':data1['dc']+data2['dc']+data3['dc'],
                    'dc_zj':data1['dc_zj']+data2['dc_zj']+data3['dc_zj'],
                    'kc':data1['kc']+data2['kc']+data3['kc'],
                    'kc_zj':data1['kc_zj']+data2['kc_zj']+data3['kc_zj'],
                    'jkd':data1['jkd']+data2['jkd']+data3['jkd'],
                    }
        data_item = {'data1':data1,'data2':data2,'data3':data3,'data4':data4}
        return data_item

    # 连接sql server 获取净多单数据
    def content_mssql(self, param,num):
        con = pymssql.connect(server="172.0.10.59", user="gt", password="server123!@#", database="GtData")
        cur = con.cursor()
        sql = "select top %s Date,Number2-Number3 from TradingTotalView where Variety=%s and MemberName='前20会员合计'  order by date desc"
        cur.execute(sql,(num,param))
        result = cur.fetchall()
        cur.close()
        con.close()
        return result

    # 净空单
    def jkd(self,num):
        self.logger.info('正在采集净空单...')
        data1 = self.content_mssql('if',num)
        data2 = self.content_mssql('ih',num)
        data3 = self.content_mssql('ic',num)
        data_item = {}
        for i in data1:
            data_item[i[0]] = i[1]
        for i in data2:
            if i[0] in data_item:
                data_item[i[0]] += i[1]
        for i in data3:
            if i[0] in data_item:
                data_item[i[0]] += i[1]
        return data_item

    def ReDianApi(self,ids):
        '''热点板块中的数据'''
        datas = []
        yesterday = str(self.today- datetime.timedelta(days=1))[0:10]
        # 区间涨跌幅
        aa = w.wsee(ids,
                    "sec_pq_pct_chg_tmc_wavg,sec_ncashinflow_d_sum_chn,sec_nclosinginflow_d_sum_chn,sec_nopeninginflow_d_sum_chn",
                    "startDate=%s;endDate=%s;DynamicTime=1;tradeDate=%s"% (yesterday.replace('-',''),str(self.today)[0:10].replace('-',''),str(self.today)[0:10].replace('-','')))
        data = aa.Data
        datas.append('%.2f%%' % data[0][0])
        datas.append('%.2f' % (data[1][0] / 100000000))
        datas.append('%.2f' % (data[2][0] / 100000000))
        datas.append('%.2f' % (data[3][0] / 100000000))
        return datas
    def redianId(self):
        file = open('config', encoding='utf-8').read()
        item = {}
        for i in file.split('\n'):
            list1 = i.split(',')
            item[list1[0]] = list1[1]
        return item
    def rdbk(self):
        '''热点板块'''
        logger.info('正在采集热点板块...')
        item = self.redianId()
        item_z = {}
        item_j = {}
        for k, v in item.items():
            data = self.ReDianApi(k)
            if '-' in data[0]:
                item_j[v] = data
            else:
                item_z[v] = data

        item_z = sorted(item_z.items(), key=lambda v: v[1][0], reverse=False)
        item_j = sorted(item_j.items(), key=lambda v: v[1][0], reverse=True)

        for i in range(len(item_z)):
            item_j.append(item_z[i])
        xd = item_j[0:5][::-1]
        sz = item_j[-5:]
        data_item = {'data1':sz,'data2':xd}
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
        sql = 'insert into daily_guzhi (date,data_items,png_items,content_items) values (%s,%s,%s,%s)'
        cur.execute(sql, (str(self.today)[:10],data_items,png_items,content_items))
        con.commit()
        con.close()
        self.logger.info('股指信息写入成功!')

    # wind 获取收盘价
    def kqjc_close_api(self, param1, param2, num):
            oneday = datetime.timedelta(days=1)
            lastday = self.today - num * oneday
            wData = w.edb('%s,%s' % (param1, param2), str(lastday)[:10], str(self.today)[:10], "Fill=Previous")
            data = wData.Data
            date = wData.Times
            data_list = [(str(date[i]), data[0][i]- data[1][i]) for i in range(len(date)) if
                         data[0][i] > 0 and data[1][i] > 0]
            return data_list

    # 期限价差
    def qxjc(self,param1,param2,param3,param4,param5,param6,num):
        self.logger.info('正在采集期货行情...')
        data1 = self.kqjc_close_api(param1,param2,num)
        data2 = self.kqjc_close_api(param3,param4,num)
        data3 = self.kqjc_close_api(param5,param6,num)
        data_item = {'data1':data1,'data2':data2,'data3':data3}
        return data_item

    def main(self):
        w.start()
        qzxx_data_item = self.qhhq("IF1906.CFE","IH1906.CFE","IC1906.CFE",5)
        zshg_data_item = self.qhhq("000300.SH","000016.SH","000905.SH",5)
        qxjc_data_item = self.qxjc("000300.SH","IF1906.CFE","000016.SH","IH1906.CFE","000905.SH","IC1906.CFE",100)
        kcjc_data_item = self.qxjc("IF1906.CFE","IF1909.CFE","IH1906.CFE","IH1909.CFE","IC1906.CFE","IC1909.CFE",100)

        jkcc_data_item = self.jkcc()
        jkd_data_item = self.jkd(300)
        rdbk_data_item = self.rdbk()

        data_items = {'qzxx_data_item':qzxx_data_item,'zshg_data_item':zshg_data_item,'jkcc_data_item':jkcc_data_item,
                      'rdbk_data_item':rdbk_data_item}
        png_items = {'jkd_data_item':jkd_data_item,'qxjc_data_item':qxjc_data_item,'kcjc_data_item':kcjc_data_item}
        data_items = json.dumps(data_items)
        png_items = json.dumps(png_items)
        content_items = json.dumps({"content_list":["略"]})
        self.write_mysql(data_items,png_items,content_items)

if __name__ == '__main__':
    gz = GuZhi()
    gz.main()

