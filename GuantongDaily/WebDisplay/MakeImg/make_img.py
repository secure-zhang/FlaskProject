# -*- coding: utf-8 -*-
import time

import datetime

from config import logger,SelectDatas

import json,os
import matplotlib as mpl
import matplotlib.pyplot as plt


logger = logger('MakePng')
plt.style.use('seaborn-dark')
# 设置中文编码和负号的正常显示
plt.rcParams['font.sans-serif'] = [u'SimHei']
plt.rcParams['axes.unicode_minus'] = False
class ShuHua():
    # 存储路径
    def __init__(self):
        self.save_path = r'../static/images/shuhua/%s'
        self.dir_name = r'../static/images/shuhua/'

    def is_save_dir(self):
        # 判断是否存在文件夹
        if not os.path.exists(self.dir_name):
            os.mkdir(r'%s' % (self.dir_name))
    def shuhua_jdd(self,param,png_path_name):
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

    # 生成塑化净多单图片
    def jdd(self, param):
        self.shuhua_jdd(param['data1'], self.save_path % 'jdd1')
        self.shuhua_jdd(param['data2'], self.save_path % 'jdd2')
        self.shuhua_jdd(param['data3'], self.save_path % 'jdd3')

    def shuhua_jicha(self,param,png_path_name):
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
        ax.bar(date_list, data_list3, linewidth=0.1, color='#7CCD7C', label='基差')

        # 获取图的坐标信息
        ax = plt.gca()

        # 设置x轴显示多少个日期刻度
        xlocator = mpl.ticker.LinearLocator(10)
        ax.xaxis.set_major_locator(xlocator)

        # 为了避免x轴日期刻度标签的重叠，设置x轴刻度自动展现，并且45度倾斜
        # plt.tick_params(labelsize=25)
        fig.autofmt_xdate(rotation=45)

        plt.savefig(png_path_name,dpi=300)

    # 生成塑化基差图片
    def jicha(self, param):
        data1 = param['data1']
        data2 = param['data2']
        data3 = param['data3']
        self.shuhua_jicha(data1, self.save_path % 'jicha1')
        self.shuhua_jicha(data2, self.save_path % 'jicha2')
        self.shuhua_jicha(data3, self.save_path % 'jicha3')

    def shuhua_jiacha(self,param, png_path_name):
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
        plt.savefig(png_path_name,dpi=300)

    # 生成塑化价差图片
    def jiacha(self, param):
        self.shuhua_jiacha(param['data1'], self.save_path % 'jiacha1')
        self.shuhua_jiacha(param['data2'], self.save_path % 'jiacha2')
        self.shuhua_jiacha(param['data3'], self.save_path % 'jiacha3')

    def run(self):
        logger.info('MAKEING SHUHUA PNG...')
        #try:
        self.is_save_dir()
        S = SelectDatas()
        json_items = S.select_data('png_items', 'daily_shuhua')
        json_items = json.loads(json_items)
        self.jdd(json_items['jdd_data_item'])
        self.jicha(json_items['jicha_data_item'])
        self.jiacha(json_items['jiacha_data_item'])
        #except:
        #    logger.error('SHUHUA ERROR')
class XiangJiao():
    # 存储路径
    def __init__(self):
        self.save_path = r'../static/images/xiangjiao/%s'
        self.dir_name = '../static/images/xiangjiao/'

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
        plt.savefig(png_path_name,dpi=300)

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

    def wpqh(self,param, png_path_name):
        date_list = param['date']
        data_list1 = param['data1']
        data_list2 = param['data2']
        data_list3 = param['data3']
        data_list4 = param['data4']

        # 主次坐标
        fig, ax = plt.subplots(1, 1)
        # 共享x轴，生成次坐标轴
        ax_sub = ax.twinx()
        # 绘图
        ax.plot(date_list, data_list1, color='#6495ED', linewidth=1)
        ax.plot(date_list, data_list2, color='#228B22', linewidth=1)
        ax.plot(date_list, data_list3, color='#CD0000', linewidth=1)
        ax_sub.plot(date_list, data_list4, color='black', linewidth=1)

        # 获取图的坐标信息
        ax = plt.gca()

        # 设置x轴显示多少个日期刻度
        xlocator = mpl.ticker.LinearLocator(10)
        ax.xaxis.set_major_locator(xlocator)

        # 为了避免x轴日期刻度标签的重叠，设置x轴刻度自动展现，并且45度倾斜
        # plt.tick_params(labelsize=25)
        fig.autofmt_xdate(rotation=45)

        # 显示图形
        plt.savefig(png_path_name,dpi=300)

    def run(self):
        logger.info('MAKEING XIANGJIAO PNG...')
        try:
            self.is_save_dir()
            S = SelectDatas()
            json_items = S.select_data('png_items', 'daily_xiangjiao')
            json_items = json.loads(json_items)
            # 现货图
            xhjg_item = json_items['xhjg_data_item']
            xhkc_item = json_items['xhkc_data_item']
            self.xh(xhjg_item, self.save_path % 'xhjg')
            self.xh(xhkc_item, self.save_path % 'xhkc')
            # 基差图
            jicha_item = json_items['jicha_data_item']
            self.jicha(jicha_item['data1'],self.save_path % 'jicha')
            # 净多单图
            jdd_data_item = json_items['jdd_data_item']
            self.jdd(jdd_data_item['data1'], self.save_path % 'jdd')
            # 外盘图
            param = json_items['wpqh_data_item']
            self.wpqh(param,self.save_path % 'wpqh')
        except:
           logger.error('XIANGJIAO ERROR')
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
        ax_sub.set_yticks([0,max(data_list1)//2,max(data_list1)])

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
        self.jicha(jklr_data_item['data1'], self.save_path % 'jklr')
class GuZhi():
    # 存储路径
    def __init__(self):
        self.save_path = r'../static/images/guzhi/%s'
        self.dir_name = '../static/images/guzhi/'

    def is_save_dir(self):
        # 判断是否存在文件夹
        if not os.path.exists(self.dir_name):
            os.mkdir(r'%s' % (self.dir_name))


    def jkd(self,param, png_path_name):
        date_list = [k for k,v in param.items()]
        data_list = [abs(v) for k,v in param.items()]

        # 设置图框的大小
        fig = plt.figure(figsize=(10, 6))
        # 绘图
        plt.plot(date_list[::-1],  # x轴数据
                 data_list[::-1],  # y轴数据
                 linestyle='-',  # 折线类型
                 linewidth=1.5,  # 折线宽度
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
        plt.savefig(png_path_name)



    # 生成塑化基差图片
    def jc(self, param,png_path_name):
        data1 = param['data1']
        data2 = param['data2']
        data3 = param['data3']

        date_list1 = [i[0] for i in data1]
        data_list1 = [i[1] for i in data1]
        date_list2 = [i[0] for i in data2]
        data_list2 = [i[1] for i in data2]
        date_list3 = [i[0] for i in data3]
        data_list3 = [i[1] for i in data3]

        # 设置图框的大小
        fig = plt.figure(figsize=(10, 6))
        # 绘图
        plt.plot(date_list1,  # x轴数据
                 data_list1,  # y轴数据
                 linestyle='-',  # 折线类型
                 linewidth=1.5,  # 折线宽度
                 color='black',  # 折线颜色
                 )
        # 绘图
        plt.plot(date_list2,  # x轴数据
                 data_list2,  # y轴数据
                 linestyle='-',  # 折线类型
                 linewidth=1.5,  # 折线宽度
                 color='red',  # 折线颜色
                 )
        # 绘图
        plt.plot(date_list3,  # x轴数据
                 data_list3,  # y轴数据
                 linestyle='-',  # 折线类型
                 linewidth=1,  # 折线宽度
                 color='green',  # 折线颜色
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
        plt.savefig(png_path_name)

    def kcjc(self, param,png_path_name):
        data1 = param['data1']
        data2 = param['data2']
        data3 = param['data3']

        date_list1 = [i[0] for i in data1]
        data_list1 = [i[1] for i in data1]
        date_list2 = [i[0] for i in data2]
        data_list2 = [i[1] for i in data2]
        date_list3 = [i[0] for i in data3]
        data_list3 = [i[1] for i in data3]

        # 主次坐标
        fig, ax = plt.subplots(1, 1)
        # 共享x轴，生成次坐标轴
        ax_sub = ax.twinx()
        # 绘图
        ax.plot(date_list1,  # x轴数据
                 data_list1,  # y轴数据
                 linestyle='-',  # 折线类型
                 linewidth=1,  # 折线宽度
                 color='black',  # 折线颜色
                 )
        # 绘图
        ax.plot(date_list2,  # x轴数据
                 data_list2,  # y轴数据
                 linestyle='-',  # 折线类型
                 linewidth=1,  # 折线宽度
                 color='red',  # 折线颜色
                 )
        # 绘图
        ax_sub.plot(date_list3,  # x轴数据
                 data_list3,  # y轴数据
                 linestyle='-',  # 折线类型
                 linewidth=1,  # 折线宽度
                 color='green',  # 折线颜色
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
        plt.savefig(png_path_name)

    def run(self):
        logger.info('MAKEING GUZHI PNG...')
        self.is_save_dir()
        S = SelectDatas()
        json_items = S.select_data('png_items', 'daily_guzhi')
        json_items = json.loads(json_items)

        # 净空单图
        jkd_data_item = json_items['jkd_data_item']
        self.jkd(jkd_data_item, self.save_path % 'jkd')

        qxjc_data_item = json_items['qxjc_data_item']
        self.jc(qxjc_data_item,self.save_path %'qxjc')

        kcjc_data_item = json_items['kcjc_data_item']
        self.kcjc(kcjc_data_item,self.save_path %'kqjc')
class YuanYou():
    # 存储路径
    def __init__(self):
        self.save_path = r'../static/images/yuanyou/%s'
        self.dir_name = '../static/images/yuanyou/'

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

    def kgl(self,param,png_path_name):
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
        # plt.legend(fontsize=20, loc='upper right')
        # 显示图形
        plt.savefig(png_path_name,dpi=300)

    def kc(self,param,png_path_name):
        date_list = [i[0] for i in param]
        data_list1 = [i[1] for i in param]
        data_list2 = [i[2] for i in param]
        # 主次坐标
        fig, ax = plt.subplots(1, 1)
        # 共享x轴，生成次坐标轴
        ax_sub = ax.twinx()
        # 绘图
        ax_sub.plot(date_list, data_list1, color='black', linewidth=1, label='期货')
        ax.plot(date_list, data_list2, color='#CD0000', linewidth=1, label='现货')

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

    def cc(self,param,png_path_name):
        date_list1 = [i[0] for i in param['data1']]
        data_list1 = [i[1] for i in param['data1']]
        date_list2 = [i[0] for i in param['data2']]
        data_list2 = [i[1] for i in param['data2']]
        # 主次坐标
        fig, ax = plt.subplots(1, 1)
        # 共享x轴，生成次坐标轴
        ax_sub = ax.twinx()
        # 绘图
        ax_sub.plot(date_list1, data_list1, color='black', linewidth=1, label='期货')
        ax.plot(date_list2, data_list2, color='#CD0000', linewidth=1, label='现货')

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

    def run(self):
        logger.info('MAKEING YUANYOU PNG...')
        self.is_save_dir()
        S = SelectDatas()
        json_items = S.select_data('png_items', 'daily_yuanyou')
        json_items = json.loads(json_items)

        # 基差图
        sc_data_item = json_items['sc_data_item']
        self.jicha(sc_data_item['data1'], self.save_path % 'sc_jc')
        wti_data_item = json_items['wti_data_item']
        self.jicha(wti_data_item['data1'], self.save_path % 'wti_jc')
        brent_data_item = json_items['brent_data_item']
        self.jicha(brent_data_item['data1'], self.save_path % 'brent_jc')

        # 开工率
        kgl_data_item = json_items['kgl_data_item']
        self.kgl(kgl_data_item, self.save_path % 'kgl')

        # 库存
        kc_data_item = json_items['kc_data_item']
        self.kc(kc_data_item['data1'], self.save_path % 'kc')
        # 持仓
        cc_data_item = json_items['cc_data_item']
        self.cc(cc_data_item, self.save_path % 'cc')
class YouZhi():
    # 存储路径
    def __init__(self):
        self.save_path = r'../static/images/youzhi/%s'
        self.dir_name = '../static/images/youzhi/'

    def is_save_dir(self):
        # 判断是否存在文件夹
        if not os.path.exists(self.dir_name):
            os.mkdir(r'%s' % (self.dir_name))


    def yzlr(self,param,png_path_name):
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

    def run(self):
        logger.info('MAKEING YOUZHI PNG...')
        self.is_save_dir()
        S = SelectDatas()
        json_items = S.select_data('png_items', 'daily_youzhi')
        json_items = json.loads(json_items)
        self.yzlr(json_items['yzlr_png_item']['data1'], self.save_path % 'yzlr1')
        self.yzlr(json_items['yzlr_png_item']['data2'], self.save_path % 'yzlr2')

def main():
    ShuHua().run()
    XiangJiao().run()
    JiaChun().run()
    GuZhi().run()
    YouZhi().run()
    YuanYou().run()
if __name__ == '__main__':
    main()
    while True:
        now_time = datetime.datetime.now().strftime('%H%M')
        if now_time > '1640' and now_time <'1800':
            logger.info('%s Start ...'%now_time)
            ShuHua().run()
            XiangJiao().run()
            JiaChun().run()
            GuZhi().run()
            YouZhi().run()
        if now_time > '0830' and now_time <'0850':
            YuanYou().run()
        time.sleep(600)



