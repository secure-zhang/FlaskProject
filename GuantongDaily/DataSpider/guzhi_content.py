# -*- encoding:utf-8-*-
# 上传股指的新闻
import pymysql,time,json

def guzhi_mysql(item):
    try:
        con = pymysql.connect(host="94.191.80.61", user="alazhijia", password="root", db="GuanTongDaily", port=3306,
                              charset='utf8')
        cur = con.cursor()
        sql = 'SELECT id FROM daily_guzhi ORDER BY addTime DESC LIMIT 1'
        cur.execute(sql)
        tid = cur.fetchall()[0][0]
        sql = 'UPDATE daily_guzhi set content_items=%s  WHERE id=%s'
        cur.execute(sql,(item,tid))
        con.commit()
        con.close()
        print('股指写入数据库成功')
    except:
        print('股指写入数据库错误')

def yuanyou_mysql(item):
    try:
        con = pymysql.connect(host="94.191.80.61", user="alazhijia", password="root", db="GuanTongDaily", port=3306,
                              charset='utf8')
        cur = con.cursor()
        sql = 'SELECT id FROM daily_yuanyou ORDER BY addTime DESC LIMIT 1'
        cur.execute(sql)
        tid = cur.fetchall()[0][0]
        sql = 'UPDATE daily_yuanyou set content_items=%s  WHERE id=%s'
        cur.execute(sql,(item,tid))
        con.commit()
        con.close()
        print('原油写入数据库成功')
    except:
        print('原油写入数据库错误')

def guzhi_content(filename):
    try:
        with open('%s.txt'%filename,'r',encoding='utf-8') as f:
            file = f.read()
        content_list = file.split('?')
        data_item = {'content_list': content_list}
        data_item = json.dumps(data_item)
        return data_item
    except:
        print('%s新闻读取错误'%filename)
        input()

def main():
    data_item = guzhi_content('股指新闻')
    guzhi_mysql(data_item)
    data_item = guzhi_content('原油新闻')
    yuanyou_mysql(data_item)


    time.sleep(5)

if __name__ == '__main__':
    main()