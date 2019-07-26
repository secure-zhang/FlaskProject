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

class YuMi():
    # 存储路径
    def __init__(self):
        self.save_path = r'../static/images/yumi/%s'
        self.dir_name = '../static/images/yumi/'

    def is_save_dir(self):
        # 判断是否存在文件夹
        if not os.path.exists(self.dir_name):
            os.mkdir(r'%s' % (self.dir_name))

    def three_years(self,param,png_path_name):
        date = param['date']

        data_list17 = [i[1] for i in param['data_list17']]
        data_list18 = [i[1] for i in param['data_list18']]
        data_list19 = [i[1] for i in param['data_list19']]
        # 设置图框的大小
        fig = plt.figure(figsize=(10, 6))
        # 绘图

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
                 color='red',  # 折线颜色
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
        # plt.show()

    def run(self):
        logger.info('MAKEING YUMI PNG...')
        self.is_save_dir()
        S = SelectDatas()
        json_items = S.select_data('png_items', 'daily_yumi')
        json_items = json.loads(json_items)
        self.three_years(json_items['xhjg_png_item'], self.save_path % 'xhjg')
        self.three_years(json_items['ymkc_png_item'], self.save_path % 'ymkc')
        self.three_years(json_items['jckr_png_item'], self.save_path % 'jklr')
        self.three_years(json_items['sdwf_png_item'], self.save_path % 'sdwf')


if __name__ == '__main__':
    YuMi().run()