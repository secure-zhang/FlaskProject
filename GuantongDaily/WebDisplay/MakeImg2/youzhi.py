# -*- coding: utf-8 -*-
from config import logger,SelectDatas
import json,os
import matplotlib as mpl
import matplotlib.pyplot as plt
import itertools as it
plt.style.use('bmh')
# 设置中文编码和负号的正常显示
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False

class YouZhi():
    def __init__(self,logger):
        self.save_path = r'../static/images/jiachun/%s'
        self.dir_name = '../static/images/jiachun/'
        self.logger = logger


    def is_save_dir(self):
        # 判断是否存在文件夹
        if not os.path.exists(self.dir_name):
            os.mkdir(r'%s' % (self.dir_name))

    def xh(self,param,png_path_name):
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
        plt.legend(fontsize=20, loc='upper right')
        # 显示图形
        plt.savefig(png_path_name)

    def run(self):
        self.logger.info('MAKEING YOUZHI PNG...')
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
        pz_list = []
        for k,v in tid_item.items():
            for k2,v2 in v.items():
                pz_list.append(k+'-'+k2)
        res = list(it.permutations(pz_list,2))
        print(res)
        print(len(res))
        for i in res:
            print(i)
            # SelectDatas.select_target_datas()
        # self.xh(xhkc_item, self.save_path % 'xhkc')


if __name__ == '__main__':
    yz = YouZhi(logger('MakePng'))
    yz.run()