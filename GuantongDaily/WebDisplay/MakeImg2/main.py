# -*- coding: utf-8 -*-
from config import logger
# from guzhi import GuZhi
# from jiachun import JiaChun
# from shuhua import ShuHua
# from xiangjiao import XiangJiao
from youzhi import YouZhi


def run():
    YouZhi(logger('MakePng')).run()


if __name__ == '__main__':
    run()

