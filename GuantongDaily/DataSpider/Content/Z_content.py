import json,pymysql
class Content:
    def __init__(self):
        self.con = pymysql.connect(host="94.191.80.61", user="alazhijia", password="root", db="GuanTongDaily", port=3306,
                              charset='utf8')
    def yuanyou_gdzj(self,item):
        try:
            cur = self.con.cursor()
            sql = 'SELECT id FROM daily_yuanyou ORDER BY addTime DESC LIMIT 1'
            cur.execute(sql)
            tid = cur.fetchall()[0][0]
            sql = 'UPDATE daily_yuanyou set content1_items=%s  WHERE id=%s'
            cur.execute(sql,(item,tid))
            self.con.commit()
            print('原油信息速递写入数据库成功')
        except:
            print('原油信息速递写入数据库错误')

    def yuanyou_xxsd(self,item):
        try:
            cur = self.con.cursor()
            sql = 'SELECT id FROM daily_yuanyou ORDER BY addTime DESC LIMIT 1'
            cur.execute(sql)
            tid = cur.fetchall()[0][0]
            sql = 'UPDATE daily_yuanyou set content2_items=%s  WHERE id=%s'
            cur.execute(sql,(item,tid))
            self.con.commit()
            print('原油观点总结写入数据库成功')
        except:
            print('原油观点总结写入数据库错误')

    def guzhi(self,item):
        try:
            cur = self.con.cursor()
            sql = 'SELECT id FROM daily_guzhi ORDER BY addTime DESC LIMIT 1'
            cur.execute(sql)
            tid = cur.fetchall()[0][0]
            sql = 'UPDATE daily_guzhi set content_items=%s  WHERE id=%s'
            cur.execute(sql,(item,tid))
            self.con.commit()
            print('股指写入数据库成功')
        except:
            print('股指写入数据库错误')
    def jiachun(self,item):
        try:
            cur = self.con.cursor()
            sql = 'SELECT id FROM daily_jiachun ORDER BY addTime DESC LIMIT 1'
            cur.execute(sql)
            tid = cur.fetchall()[0][0]
            sql = 'UPDATE daily_jiachun set content_items=%s  WHERE id=%s'
            cur.execute(sql,(item,tid))
            self.con.commit()
            print('甲醇写入数据库成功')
        except:
            print('甲醇写入数据库错误')

    def shuhua(self, item):
        try:
            cur = self.con.cursor()
            sql = 'SELECT id FROM daily_shuhua ORDER BY addTime DESC LIMIT 1'
            cur.execute(sql)
            tid = cur.fetchall()[0][0]
            sql = 'UPDATE daily_shuhua set content_items=%s  WHERE id=%s'
            cur.execute(sql, (item, tid))
            self.con.commit()
            print('塑化写入数据库成功')
        except:
            print('塑化写入数据库错误')
    def pta(self,item):
        try:
            cur = self.con.cursor()
            sql = 'SELECT id FROM daily_pta ORDER BY addTime DESC LIMIT 1'
            cur.execute(sql)
            tid = cur.fetchall()[0][0]
            sql = 'UPDATE daily_pta set content_items=%s  WHERE id=%s'
            cur.execute(sql,(item,tid))
            self.con.commit()
            print('PTA写入数据库成功')
        except:
            print('PTA写入数据库错误')

    def xiangjiao(self, item):
        try:
            cur = self.con.cursor()
            sql = 'SELECT id FROM daily_xiangjiao ORDER BY addTime DESC LIMIT 1'
            cur.execute(sql)
            tid = cur.fetchall()[0][0]
            sql = 'UPDATE daily_xiangjiao set content_items=%s  WHERE id=%s'
            cur.execute(sql, (item, tid))
            self.con.commit()
            print('橡胶写入数据库成功')
        except:
            print('橡胶写入数据库错误')
    def youzhi(self, item):
        try:
            cur = self.con.cursor()
            sql = 'SELECT id FROM daily_xiangjiao ORDER BY addTime DESC LIMIT 1'
            cur.execute(sql)
            tid = cur.fetchall()[0][0]
            sql = 'UPDATE daily_xiangjiao set content_items=%s  WHERE id=%s'
            cur.execute(sql, (item, tid))
            self.con.commit()
            print('橡胶写入数据库成功')
        except:
            print('橡胶写入数据库错误')

    def content(self,filename):
        with open('%s.txt'%filename,'r',encoding='utf-8') as f:
            lines_list = f.readlines()
        for line in lines_list:
            line_list = line.strip().split('--')
            if 'yuanyou' in line:
                if 'gdzj' in line:
                    content_list = line_list[-1].split('?')
                    data_item = {'content_list': content_list}
                    data_item = json.dumps(data_item)
                    self.yuanyou_gdzj(data_item)
                if 'xxsd' in line:
                    content_list = line_list[-1].split('?')
                    data_item = {'content_list': content_list}
                    data_item = json.dumps(data_item)
                    self.yuanyou_xxsd(data_item)
            else:
                content_list = line_list[-1].split('?')
                data_item = {'content_list': content_list}
                data_item = json.dumps(data_item)
                if 'guzhi' in line:
                    self.guzhi(data_item)
                if 'jiachun' in line:
                    self.jiachun(data_item)
                if 'shuhua' in line:
                    self.shuhua(data_item)
                if 'pta' in line:
                    self.pta(data_item)
                if 'xiangjiao' in line :
                    self.xiangjiao(data_item)
                if 'youzhi' in line :
                    self.youzhi(data_item)
        input()

if __name__ == '__main__':
    Content().content('新闻')
