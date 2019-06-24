

# -*- coding: utf-8 -*-
import json,os,pymysql
import matplotlib as mpl
import matplotlib.pyplot as plt
import itertools as it
plt.style.use('bmh')
# 设置中文编码和负号的正常显示
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False

class YouZhi():
    def __init__(self):
        self.save_path = r'./static/images/youzhi/%s'
        self.dir_name = './static/images/youzhi/'


    def is_save_dir(self):
        # 判断是否存在文件夹
        if not os.path.exists(self.dir_name):
            os.mkdir(r'%s' % (self.dir_name))

    def kpztljc(self,param,png_path_name):
        date = param['date']

        data_list15 = [i[1] for i in param['data_list15']]
        data_list16 = [i[1] for i in param['data_list16']]
        data_list17 = [i[1] for i in param['data_list17']]
        data_list18 = [i[1] for i in param['data_list18']]
        data_list19 = [i[1] for i in param['data_list19']]
        # 设置图框的大小
        fig = plt.figure(figsize=(10, 6))
        # 绘图
        plt.plot(date[:len(data_list15)],  # x轴数据
                 data_list15,  # y轴数据
                 linestyle='-',  # 折线类型
                 linewidth=2,  # 折线宽度
                 color='#FF7F50',  # 折线颜色
                 label='2015')  # 点的填充色

        plt.plot(date[:len(data_list16)],  # x轴数据
                 data_list16,  # y轴数据
                 linestyle='-',  # 折线类型
                 linewidth=2,  # 折线宽度
                 color='#5F9EA0',  # 折线颜色
                 label='2016')  #

        plt.plot(date[:len(data_list17)],  # x轴数据
                 data_list17,  # y轴数据
                 linestyle='-',  # 折线类型
                 linewidth=2,  # 折线宽度
                 color='#8B4513',  # 折线颜色
                 label='2017')

        plt.plot(date[:len(data_list18)],  # x轴数据
                 data_list18,  # y轴数据
                 linestyle='-',  # 折线类型
                 linewidth=2,  # 折线宽度
                 color='#4169E1',  # 折线颜色
                 label='2018')

        plt.plot(date[:len(data_list19)],  # x轴数据
                 data_list19,  # y轴数据
                 linestyle='-',  # 折线类型
                 linewidth=3,  # 折线宽度
                 color='#000000',  # 折线颜色
                 label='2019')
        # 获取图的坐标信息
        ax = plt.gca()

        # 设置x轴显示多少个日期刻度
        xlocator = mpl.ticker.LinearLocator(10)
        ax.xaxis.set_major_locator(xlocator)

        # 为了避免x轴日期刻度标签的重叠，设置x轴刻度自动展现，并且45度倾斜
        plt.tick_params(labelsize=20)
        fig.autofmt_xdate(rotation=45)
        # 显示图形
        plt.savefig(png_path_name)

    def select_target_datas(self,tid):
        con = pymysql.connect(host='94.191.80.61', port=3306, user='zhang', password='zhang', db='GuanTongDaily',
                              charset='utf8')
        cur = con.cursor()
        sql = "SELECT date,value FROM target_datas where tid=%s and date> '2015-01-01' ORDER BY date  "
        cur.execute(sql,tid)
        result = cur.fetchall()
        cur.close()
        con.close()
        return result


    def format_data(self, data_list,):



        # data_12 = []
        # data_13 = []
        # data_14 = []
        data_15 = []
        data_16 = []
        data_17 = []
        data_18 = []
        data_19 = []
        for data in data_list:
            # if data[0][2:4] == '15':
            #     data_12.append(data)
            # if data[0][2:4] == '16':
            #     data_13.append(data)
            # if data[0][2:4] == '17':
            #     data_14.append(data)
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

        date_list = [i[0][5:] for i in data_15]
        data_item = {'date':date_list,'data_list15':data_15,'data_list16':data_16,'data_list17':data_17,'data_list18':data_18,'data_list19':data_19}

        return data_item

    def run(self,kpztljc1,kpztljc2,pzbj1,pzbj2):
        self.is_save_dir()
        tid_item = {
            'a':{'1':'S0264410','5':'S0264411','9':'S0264412'},#
            'm':{'1':'S0264422','5':'S0264423','9':'S0264424'},
            'y':{'1':'S0264428','5':'S0264429','9':'S0264430'},
            'p':{'1':'S0264448','5':'S0264449','9':'S0264450'},
            'c':{'1':'S0264478','5':'S0264479','9':'S0264480'},
            'jd':{'1':'S0264472','5':'S0264473','9':'S0264474'},
            'cs':{'1':'S0264484','5':'S0264485','9':'S0264486'},
            'rs':{'1':'S0264436','5':'S0264437','9':'S0264438'},
            'rm':{'1':'S0264442','5':'S0264443','9':'S0264444'},
            'sr':{'1':'S0264454','5':'S0264455','9':'S0264456'},
            'cf':{'1':'S0264460','5':'S0264461','9':'S0264462'},
        }
        kpztljc1 = tid_item[kpztljc1.split('-')[0]][kpztljc1.split('-')[1]]
        kpztljc2 = tid_item[kpztljc2.split('-')[0]][kpztljc2.split('-')[1]]

        param1_item = dict(iter(self.select_target_datas(kpztljc1)))
        param2_item = dict(iter(self.select_target_datas(kpztljc2)))
        data_list = [(k,v-param2_item[k]) for k,v in param1_item.items() if k in param2_item]

        param = self.format_data(data_list)
        self.kpztljc(param,self.save_path%'kpztljc')

        pzbj1 = tid_item[pzbj1.split('-')[0]][pzbj1.split('-')[1]]
        pzbj2 = tid_item[pzbj2.split('-')[0]][pzbj2.split('-')[1]]
        param1_item = dict(iter(self.select_target_datas(pzbj1)))
        param2_item = dict(iter(self.select_target_datas(pzbj2)))
        data_list = [(k, v / param2_item[k]) for k, v in param1_item.items() if k in param2_item]
        param = self.format_data(data_list)
        self.kpztljc(param,self.save_path%'pzbj')


if __name__ == '__main__':
    yz = YouZhi()
    yz.run('a-1','c-1','a-1','a-1')