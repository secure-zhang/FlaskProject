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

if __name__ == '__main__':
    gz = GuZhi()
    gz.run()