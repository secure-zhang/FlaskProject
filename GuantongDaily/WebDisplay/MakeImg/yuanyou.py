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

if __name__ == '__main__':
    yy = YuanYou()
    yy.run()