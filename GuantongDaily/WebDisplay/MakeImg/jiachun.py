# -*- coding: utf-8 -*-
from config import logger,SelectDatas
import json,os
import matplotlib as mpl
import matplotlib.pyplot as plt


logger = logger('MakePng')
plt.style.use('bmh')
# 设置中文编码和负号的正常显示
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False

class JiaChun():
    # 存储路径
    def __init__(self):
        self.save_path = r'../static/images/jiachun/%s'
        self.dir_name = '../static/images/jiachun/'


    def is_save_dir(self):
        # 判断是否存在文件夹
        if not os.path.exists(self.dir_name):
            os.mkdir(r'%s' % (self.dir_name))

    def jicha(self,param,png_path_name):
        date_list = [i[0] for i in param]
        data_list1 = [i[1] for i in param]
        data_list2 = [i[2] for i in param]
        data_list3 = [i[3] for i in param]
        # 主次坐标
        fig, ax = plt.subplots(1, 1)
        # 共享x轴，生成次坐标轴
        ax_sub = ax.twinx()
        # 绘图
        ax_sub.plot(date_list, data_list1, color='black', linewidth=1, label='期货')
        ax_sub.plot(date_list, data_list2, color='#CD0000', linewidth=1, label='现货')
        ax.bar(date_list, data_list3, linewidth=0.5, color='#7CCD7C', label='基差')

        # 获取图的坐标信息
        ax = plt.gca()

        # 设置x轴显示多少个日期刻度
        xlocator = mpl.ticker.LinearLocator(10)
        ax.xaxis.set_major_locator(xlocator)

        # 为了避免x轴日期刻度标签的重叠，设置x轴刻度自动展现，并且45度倾斜
        # plt.tick_params(labelsize=25)
        fig.autofmt_xdate(rotation=45)

        plt.savefig(png_path_name,dpi=300)
        # plt.show()

    def pplr(self,param,png_path_name):
        date_list = [i[0] for i in param]
        data_list1 = [i[1] for i in param]
        data_list2 = [i[2] for i in param]
        data_list3 = [i[3] for i in param]
        # 主次坐标
        fig, ax = plt.subplots(1, 1)
        # 共享x轴，生成次坐标轴
        ax_sub = ax.twinx()

        # 绘图
        ax_sub.plot(date_list, data_list1, color='black', linewidth=1, label='期货')
        ax.plot(date_list, data_list2, color='#CD0000', linewidth=1, label='现货')
        ax.bar(date_list, data_list3, linewidth=0.5, color='#7CCD7C', label='基差')
        # ax_sub.set_yticks([max(data_list1)//8,max(data_list1)*2//8,max(data_list1)*3//8,max(data_list1)*4//8,max(data_list1)*5//8,max(data_list1)*6//8,max(data_list1)*7/8,max(data_list1)])
        ax_sub.set_yticks([i*500 for i in range(9)])
        ax.set_yticks([i*1000 for i in range(-2,12)])

        # 获取图的坐标信息
        ax = plt.gca()

        # 设置x轴显示多少个日期刻度
        xlocator = mpl.ticker.LinearLocator(10)
        ax.xaxis.set_major_locator(xlocator)

        # 为了避免x轴日期刻度标签的重叠，设置x轴刻度自动展现，并且45度倾斜
        # plt.tick_params(labelsize=25)
        fig.autofmt_xdate(rotation=45)

        plt.savefig(png_path_name,dpi=300)
        # plt.show()

    def jdd(self,param, png_path_name):

        date_list = [i[0] for i in param]
        data_list = [i[1] for i in param]

        # 设置图框的大小
        fig = plt.figure(figsize=(10, 6))
        # 绘图
        plt.plot(date_list[::-1],  # x轴数据
                 data_list[::-1],  # y轴数据
                 linestyle='-',  # 折线类型
                 linewidth=2,  # 折线宽度
                 color='black',  # 折线颜色
                 )

        # 获取图的坐标信息
        ax = plt.gca()
        # 设置x轴显示多少个日期刻度
        xlocator = mpl.ticker.LinearLocator(10)
        ax.xaxis.set_major_locator(xlocator)

        # 为了避免x轴日期刻度标签的重叠，设置x轴刻度自动展现，并且45度倾斜
        plt.tick_params(labelsize=18)
        fig.autofmt_xdate(rotation=45)

        # 显示图形
        plt.savefig(png_path_name,dpi=300)

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
        # 显示图形
        plt.savefig(png_path_name,dpi=300)

    def run(self):
        logger.info('MAKEING JIACHUN PNG...')
        self.is_save_dir()
        S = SelectDatas()
        json_items = S.select_data('png_items', 'daily_jiachun')
        json_items = json.loads(json_items)

        # 基差图
        jicha_item = json_items['jicha_data_item']
        self.jicha(jicha_item['data1'], self.save_path % 'jicha')

        # 价差图
        jicha_item = json_items['jiacha_data_item']
        self.jicha(jicha_item['data1'], self.save_path % 'jiacha')

        # 净多单图
        jdd_data_item = json_items['jdd_data_item']
        self.jdd(jdd_data_item['data1'], self.save_path % 'jdd')

        # 库存图
        xhkc_item = json_items['xhkc_data_item']
        self.xh(xhkc_item, self.save_path % 'xhkc')

        # PP利润
        pplr_data_item = json_items['pplr_data_item']
        self.pplr(pplr_data_item['data1'], self.save_path % 'pplr')
        #
        # # 进口利润
        jklr_data_item = json_items['jklr_data_item']
        jklr_data_item['data1'].sort()
        self.jicha(jklr_data_item['data1'], self.save_path % 'jklr')

if __name__ == '__main__':
    jc = JiaChun()
    jc.run()