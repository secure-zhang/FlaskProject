import time

import datetime
import os

if __name__ == '__main__':

    while True:
        now_time = datetime.datetime.now().strftime('%H%M')
        if now_time > '1340' and now_time < '1750':
            os.system('python jiachun.py')
            os.system('python guzhi.py')
            os.system('python shuhua.py')
            os.system('python pta.py')
            os.system('python youzhi.py')
            os.system('python xiangjiao.py')
        if now_time > '0820' and now_time < '0850':
            os.system('python yuanyou.py')

        time.sleep(600)
