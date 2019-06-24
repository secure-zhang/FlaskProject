# -*- coding: utf-8 -*-

import pymysql

class SelectDatas():
    def select_cjcc(self):
        # 94.191.80.61
        # 127.0.0.1
        con = pymysql.connect(host='94.191.80.61', port=3306, user='zhang', password='zhang', db='hxcce', charset='utf8')
        cur = con.cursor()
        sql = "SELECT * FROM WindComFutures ORDER BY DATE DESC LIMIT 20"
        nums = cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        con.close()
        return nums,result

    def select_data(self,items,db_name):
        con = pymysql.connect(host='94.191.80.61', port=3306, user='zhang', password='zhang', db='GuanTongDaily', charset='utf8')
        cur = con.cursor()
        sql = "SELECT %s FROM %s ORDER BY addTime DESC LIMIT 1"%(items,db_name)
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        con.close()
        return result[0][0]

    def select_content(self,items,db_name):
        con = pymysql.connect(host='94.191.80.61', port=3306, user='zhang', password='zhang', db='GuanTongDaily', charset='utf8')
        cur = con.cursor()
        sql = "SELECT %s FROM %s ORDER BY addTime DESC LIMIT 1"%(items,db_name)
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        con.close()
        return result[0][0]
