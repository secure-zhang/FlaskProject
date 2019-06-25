# -*- encoding:utf-8-*-
# 采集股原油日报所需要的所有数据
import json
from config import logger
from WindPy import *
from bs4 import BeautifulSoup
import requests,datetime,re,pymssql,pymysql
logger = logger('GUZHI')
class YuanYou():
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:67.0) Gecko/20100101 Firefox/67.0',
               'Host':'www.99qh.com'}
    logger=logger
    def __init__(self):
        self.today = datetime.datetime.today()

        # 品种分析解析列表页面

    def pzfx_parse_lsit_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find('td', class_='s_99qh_line6').table
        if not table:
            return
        # <span class="s_99qh_12px"><a href="http://www.99qh.com/s/news20190531165501060.shtml" target="_blank"
        span_list = table.find_all('span', class_='s_99qh_12px')
        url_list = [span.a.attrs['href'] for span in span_list if '原油' in span.text]
        return url_list

        # 品种分析解析详情页面

    def pzfx_parse_html(self, html):
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find('div', id='div_content').text
        # 总结以后,操作以前
        content = re.search('总结：(.*?)技术', content)
        if content:
            content_list = content.group()[3:].split('。')[0:-1]
            new_content = '。'.join(content_list)
            return new_content
        return None

        # 品种分析获取页面

    def pzfx_get_html(self, url):
        html = requests.get(url=url, headers=self.header)
        if html.status_code == 200:
            return html.text
        return None

        # 品种分析

    def pzfx(self):
        self.logger.info('正在采集品种分析内容...')
        url = 'http://www.99qh.com/s/column-list.aspx?tag=RLYSCPL&date=%s'%str(self.today)[:10]
        # url = 'http://www.99qh.com/s/column-list.aspx?tag=RLYSCPL&date=%s' % '2019-06-13'
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
        return {'jg':jg,'zd':'%.2f'%zd}

    # 期货行情
    def qhhq(self,param1,param2,param3,num):
        self.logger.info('正在采集期货行情...')
        data1 = self.close_api(param1,num)
        data2 = self.close_api(param2,num)
        data3 = self.close_api(param3,num)
        data_item = {'data1':data1,'data2':data2,'data3':data3}
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
        return {'jg':jg,'zd':'%.2f'%zd}

    # 现货行情
    def xhhq(self,param1,param2,param3,num):
        self.logger.info('正在采集现货行情...')
        data1 = self.edb_api(param1,num)
        data2 = self.edb_api(param2,num)
        data3 = self.edb_api(param3,num)
        data_item = {'data1':data1,'data2':data2,'data3':data3}
        return data_item

    def SC_jiacha_api(self, param1, param2,param3, num):
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday
        wData = w.wsd('%s,%s,%s' % (param1, param2,param3), "close", str(lastday)[:10], str(self.today)[:10], "")
        data = wData.Data
        date = wData.Times

        data_list = [(str(date[i]), data[0][i], data[1][i]*data[2][i], data[1][i]*data[2][i] - data[0][i] ) for i in range(len(date)) if
                     data[0][i] > 0 and data[1][i] > 0]
        return data_list

        # 基差

    def sc_jicha(self, param1, param2, param3,num):
        self.logger.info('正在采集SC基差...')
        data1 = self.SC_jiacha_api(param1, param2,param3, num)
        data_item = {'data1': data1}
        return data_item

    def WTI_jiacha_api(self, param1, param2, num):
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday
        wData = w.wsd('%s,%s' % (param1, param2), "close", str(lastday)[:10], str(self.today)[:10], "")
        data = wData.Data
        date = wData.Times
        data_list = [(str(date[i]), data[0][i], data[1][i], data[0][i] - data[1][i]) for i in range(len(date)) if
                     data[0][i] > 0 and data[1][i] > 0]
        return data_list

        # 基差

    def WTI_jicha(self, param1, param2, num):
        self.logger.info('正在采集WTI和Brent基差...')
        data1 = self.WTI_jiacha_api(param1, param2, num)
        data_item = {'data1': data1}
        return data_item

    #  价差 wind获取大量价差指标数据
    def kgl(self,param1):
        self.logger.info('正在采集开工率...')
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
        date_list = ['2019-'+i[0][5:7] for i in data_18]
        data_itme = {'date':date_list,'data_list15':data_15,'data_list16':data_16,'data_list17':data_17,'data_list18':data_18,'data_list19':data_19}
        return data_itme

    def kc_api(self, param1, param2, num):
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday
        wData = w.wsd('%s,%s' % (param1, param2), "close", str(lastday)[:10], str(self.today)[:10], "")
        data = wData.Data
        date = wData.Times
        data_list = [(str(date[i]), data[0][i], data[1][i]) for i in range(len(date)) if
                     data[0][i] > 0 and data[1][i] > 0]
        return data_list

        # 基差

    def kc(self, param1, param2, num):
        self.logger.info('正在采集库存...')
        data1 = self.kc_api(param1, param2, num)
        data_item = {'data1': data1}
        return data_item

    def cc_api(self, param1, param2, num):
        oneday = datetime.timedelta(days=1)
        lastday = self.today - num * oneday
        wData = w.wsd('%s,%s' % (param1, param2), "close", str(lastday)[:10], str(self.today)[:10], "")
        data = wData.Data
        date = wData.Times
        data_list = [(str(date[i]), data[0][i]- data[1][i]) for i in range(len(date)) if
                     data[0][i] > 0 and data[1][i] > 0]
        return data_list

        # 基差

    def cc(self, param1, param2,param3, param4, num):
        self.logger.info('正在采集持仓...')
        data1 = self.cc_api(param1, param2, num)
        data2 = self.cc_api(param3, param4, num)
        data_item = {'data1': data1,'data2':data2}
        return data_item

    def write_mysql(self, data_items,png_items,content1_items,content2_items):
        con = pymysql.connect(host="94.191.80.61", user="alazhijia", password="root", db="GuanTongDaily", port=3306,
                              charset='utf8')
        cur = con.cursor()
        # 删除
        # drop_sql = 'delete from daily_shuhua where date=%s'
        # cur.execute(drop_sql,str(self.today))
        # con.commit()
        # 添加
        sql = 'insert into daily_yuanyou (date,data_items,png_items,content1_items,content2_items) values (%s,%s,%s,%s,%s)'
        cur.execute(sql, (str(self.today)[:10],data_items,png_items,content1_items,content2_items))
        con.commit()
        con.close()
        self.logger.info('原油信息写入成功!')


    def main(self):
        w.start()
        content_list = self.pzfx()
        qhhq_data_item = self.qhhq("CLQ19E.NYM","BQ19E.IPE","SC1907.INE",5)
        xhhq_data_item = self.xhhq("s5111903","s5111905","s0031528",5)

        sc_data_item = self.sc_jicha("m0330182","s0031528","M0000185",300)
        wti_data_item = self.WTI_jicha("s5111903","s0180896",300)
        brent_data_item = self.WTI_jicha("s5111905","s0260036",300)
        kgl_data_item = self.kgl("s5105070")
        kc_data_item = self.kc("s0069597","s5120059",300)
        cc_data_item = self.cc("s0108040","s0108041","s0108044","s0108043",300)
        data_items = { 'qhhq_data_item': qhhq_data_item, 'xhhq_data_item': xhhq_data_item}
        png_items = {'sc_data_item': sc_data_item, 'wti_data_item': wti_data_item,
                     'brent_data_item': brent_data_item, 'kgl_data_item': kgl_data_item,
                     'kc_data_item': kc_data_item,
                     'cc_data_item': cc_data_item}
        data_items = json.dumps(data_items)
        png_items = json.dumps(png_items)
        content1_items = json.dumps({"content_list":content_list})
        content2_items = json.dumps({"content_list":['略']})
        self.write_mysql(data_items,png_items,content1_items,content2_items)



if __name__ == '__main__':
    yy = YuanYou()
    yy.main()
