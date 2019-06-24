# -*- encoding:utf-8-*-
# 采集橡胶日报所需要的所有数据
import json
from config import logger
from WindPy import *
from bs4 import BeautifulSoup
import requests,datetime,re,pymssql,pymysql
logger = logger('SHUHUA')

class XiangJiao():
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0',
               'Host':'www.99qh.com'}
    logger=logger
    def __init__(self):
        self.today = datetime.datetime.today()

    # 品种分析解析列表页面
    def pzfx_parse_lsit_html(self,html):
        soup = BeautifulSoup(html,'lxml')
        table = soup.find('td', class_='s_99qh_line6').table
        if not table:
            return
        # <span class="s_99qh_12px"><a href="http://www.99qh.com/s/news20190531165501060.shtml" target="_blank"
        span_list = table.find_all('span', class_='s_99qh_12px')
        url_list = [span.a.attrs['href'] for span in span_list]
        return url_list

    # 品种分析解析详情页面
    def pzfx_parse_html(self,html):
        soup = BeautifulSoup(html,'lxml')
        content = soup.find('div',id='div_content').text
        # 总结以后,操作以前
        content = re.search('总结：(.*?)从技术', content)
        if content:
            content_list = content.group()[3:].split('。')[0:-1]
            new_content = '。'.join(content_list)
            return new_content
        return None

    # 品种分析获取页面
    def pzfx_get_html(self,url):
        html = requests.get(url=url,headers=self.header)
        if html.status_code == 200:
            return html.text
        return None

    # 品种分析
    def pzfx(self):
        self.logger.info('正在采集品种分析内容...')
        url = 'http://www.99qh.com/s/column-list.aspx?tag=XJSCPL&date=%s'%str(self.today)[:10]
        # url = 'http://www.99qh.com/s/column-list.aspx?tag=XJSCPL&date=%s'%'2019-06-06'
        html = self.pzfx_get_html(url)
        if not html:
            self.logger.error('未获取品种分析页面')
            return ['略']
        url_list = self.pzfx_parse_lsit_html(html)
        if not url_list:
            self.logger.error('未获取品种分析页面')
            return ['略']
        content_list = []
        for url in url_list:
            html = self.pzfx_get_html(url)
            content = self.pzfx_parse_html(html)
            if not content:
                continue
            content_list.append(content)
        if not content_list:
            return ['略']
        return content_list

    # wind 获取收盘价
    def close_api(self, param,num):
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday

        wData = w.wsd(param, "close", str(lastday)[:10], str(self.today)[:10], "")
        data = wData.Data[0]
        if len(data) < 3:
            return self.close_api(param,num+1)
        jg = data[-1]
        zd = data[-1] - data[-2]
        if data[-1] == data[-2]:
            zd = data[-1] -data[-3]
        return {'jg':jg,'zd':zd}

    # 期货行情
    def qhhq(self,param1,param2,num):
        self.logger.info('正在采集期货行情...')
        data1 = self.close_api(param1,num)
        data2 = self.close_api(param2,num)
        data_item = {'data1':data1,'data2':data2}
        return data_item


    # wind 获取指标数据
    def edb_api(self, param,num):
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday

        wData = w.edb(param, str(lastday)[:10], str(self.today)[:10], "Fill=Previous")

        data = wData.Data[0]
        if len(data) < 3:
            return self.edb_api(param,num+1)
        jg = data[-1]
        zd = data[-1] - data[-2]
        if data[-1] == data[-2]:
            zd = data[-1] -data[-3]
        return {'jg':jg,'zd':zd}

    # 现货行情
    def xhhq(self,param1,num):
        self.logger.info('正在采集现货行情...')
        data1 = self.edb_api(param1,num)
        data_item = {'data1':data1}
        return data_item

    # wind获取大量基差指标数据
    def edb_jicha_api(self,param,param2,num):
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday
        wData = w.edb('%s,%s'%(param,param2), str(lastday)[:10], str(self.today)[:10], "Fill=Previous")
        data = wData.Data
        date = wData.Times
        data_list = [(str(date[i]),data[0][i], data[1][i], data[0][i] - data[1][i]) for i in range(len(date)) if data[0][i]>0 and data[1][i]>0 ]
        return data_list

    # 基差
    def jicha(self,param1,param2,num):
        self.logger.info('正在采集基差...')
        data1 = self.edb_jicha_api(param1,param2,num)
        data_item = {'data1':data1}
        return data_item

    # 连接sql server 获取净多单数据
    def content_mssql(self, param,num):
        con = pymssql.connect(server="172.0.10.59", user="gt", password="server123!@#", database="GtData")
        cur = con.cursor()
        sql = "select top %s Date,Number2-Number3 from TradingTotalView where Variety=%s and MemberName='前20会员合计'  order by date desc"
        cur.execute(sql, (num,param))
        result = cur.fetchall()
        cur.close()
        con.close()
        return result

    # 净多单
    def jdd(self,num):
        self.logger.info('正在采集净多单...')
        # 聚丙烯
        data1 = self.content_mssql('ru',num)
        data_item = {'data1': data1}
        return data_item


    #  价差 wind获取大量价差指标数据
    def xhjg(self,param1):
        self.logger.info('正在采集现货价格或者现货库存...')
        wData = w.edb('%s'%(param1), '2015-01-01', str(self.today)[:10], "Fill=Previous")
        date = wData.Times
        data1 = wData.Data[0]
        data_list = [(str(date[i]),data1[i]) for i in range(len(date))]

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

        date_list = [i[0][5:] for i in data_16]
        data_itme = {'date':date_list,'data_list15':data_15,'data_list16':data_16,'data_list17':data_17,'data_list18':data_18,'data_list19':data_19}
        return data_itme


    def wpqh(self,  param1, param2, param3,param4,num):
        # 新加坡橡胶:RSS3	  新加坡橡胶:TSR20(FOB)	东京橡胶:RSS3	国内期货
        self.logger.info('正在采集外盘期货...')
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday
        wData = w.edb('%s,%s,%s,%s' % (param1, param2, param3,param4), str(lastday)[:10], str(self.today)[:10], "Fill=Previous")
        date = wData.Times
        date = [str(i) for i in date]
        data1 = wData.Data[0]
        data2 = wData.Data[1]
        data3 = wData.Data[2]
        data4 = wData.Data[3]
        data_item = {'data1':data1,'data2':data2,'data3':data3,'data4':data4,'date':date}
        return data_item

    def write_mysql(self, data_items,png_items):
        con = pymysql.connect(host="94.191.80.61", user="alazhijia", password="root", db="GuanTongDaily", port=3306,
                              charset='utf8')
        cur = con.cursor()
        # 删除
        # drop_sql = 'delete from daily_shuhua where date=%s'
        # cur.execute(drop_sql,str(self.today))
        # con.commit()
        # 添加
        sql = 'insert into daily_xiangjiao (date,data_items,png_items) values (%s,%s,%s)'
        cur.execute(sql, (str(self.today)[:10],data_items,png_items))
        con.commit()
        con.close()
        self.logger.info('橡胶信息写入成功!')


    def main(self):
        w.start()
        content_list = self.pzfx()
        qhhq_data_item = self.qhhq("RU1909.SHF","RU2001.SHF",5)
        xhhq_data_item = self.xhhq("s5016816",5)
        jicha_data_item = self.jicha("s5016816","M0066359",300)
        jdd_data_item = self.jdd(300)
        xhjg_data_item = self.xhjg("s5016816")
        xhkc_data_item = self.xhjg("s0163835")
        wpqh_data_item = self.wpqh("s5016922","s5016926","s5016928","m0066359",300)
        data_items = {'content_list':content_list,'qhhq_data_item':qhhq_data_item,'xhhq_data_item':xhhq_data_item}
        png_items = {'jicha_data_item':jicha_data_item,'jdd_data_item':jdd_data_item,'xhjg_data_item':xhjg_data_item,'xhkc_data_item':xhkc_data_item,'wpqh_data_item':wpqh_data_item}
        data_items = json.dumps(data_items)
        png_items = json.dumps(png_items)
        self.write_mysql(data_items,png_items)


if __name__ == '__main__':
    xj = XiangJiao()
    xj.main()
