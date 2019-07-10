#
# import json,os
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# from config import logger,SelectDatas
#
#
# logger = logger('MakePng')
# plt.style.use('seaborn-dark')
# # 设置中文编码和负号的正常显示
# plt.rcParams['font.sans-serif'] = [u'SimHei']
# plt.rcParams['axes.unicode_minus'] = False
#
from guzhi import GuZhi
from jiachun import JiaChun
from shuhua import ShuHua
from xiangjiao import XiangJiao


if __name__ == '__main__':
    # sh = ShuHua()
    # sh.run()
    # xj = XiangJiao()
    # xj.run()
    # jc = JiaChun()
    # jc.run()
    gz = GuZhi()
    gz.run()