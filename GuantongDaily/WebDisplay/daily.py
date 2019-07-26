# -*- coding: utf-8 -*-

from __init__ import app,login_user, login_required,login_manager,logout_user
from flask import render_template,request,redirect,url_for,session
import json
import datetime,time
from mysql_db import SelectDatas
from make_post_png import YouZhi
from make_post_png import YuMi
# 创建daily蓝图
from flask import Blueprint
daily = Blueprint('daily',__name__)

# 尿素信息
@app.route('/daily/niaoshu',methods=['GET'])
@login_required
def niaoshu():
    S= SelectDatas()
    content_item = S.select_data('content_items','daily_niaoshu')
    content_item = json.loads(content_item)
    json_items = S.select_data('data_items','daily_niaoshu')
    json_items = json.loads(json_items)
    today = str(datetime.datetime.today())[:10]
    return render_template('daily/niaoshu.html', today=today,content=content_item,items=json_items,val1=time.time())



# 油脂油料信息
@app.route('/daily/youzhi',methods=['GET','POST'])
@login_required
def youzhi():
    item = {'kpztljc1' : ['a-1+请选择','请选择'],'kpztljc2' : ['a-1+请选择','请选择'],'pzbj1' : ['a-1+请选择','请选择'],'pzbj2':  ['a-1+请选择','请选择']}
    today = str(datetime.datetime.today())[:10]
    S= SelectDatas()
    content_item = S.select_data('content_items','daily_youzhi')
    content_item = json.loads(content_item)
    json_items = S.select_data('data_items','daily_youzhi')
    json_items = json.loads(json_items)
    if request.method == 'POST':
        kpztljc1 = request.form.get('kpztljc1').split('+')
        kpztljc2 = request.form.get('kpztljc2').split('+')
        pzbj1 = request.form.get('pzbj1').split('+')
        pzbj2 = request.form.get('pzbj2').split('+')
        item['kpztljc1'] = [kpztljc1[0]+'+'+kpztljc1[1],kpztljc1[1]]
        item['kpztljc2'] = [kpztljc2[0]+'+'+kpztljc2[1],kpztljc2[1]]
        item['pzbj1'] = [pzbj1[0]+'+'+pzbj1[1],pzbj1[1]]
        item['pzbj2'] = [pzbj2[0]+'+'+pzbj2[1],pzbj2[1]]
        YouZhi().run(kpztljc1[0],kpztljc2[0],pzbj1[0],pzbj2[0])
    return render_template('daily/youzhi.html',items=json_items,content=content_item,val1=time.time(),today=today,item=item)


# 玉米信息
@app.route('/daily/yumi',methods=['GET','POST'])
# @login_required
def yumi():
    item = {'ymkqjc1' : ['c-1+请选择','请选择'],'ymkqjc2' : ['c-1+请选择','请选择'],'dfkqjc1' : ['cs-1+请选择','请选择'],'dfkqjc2':  ['cs-1+请选择','请选择']}
    today = str(datetime.datetime.today())[:10]
    S= SelectDatas()
    content_item = S.select_data('content_items','daily_yumi')
    content_item = json.loads(content_item)
    json_items = S.select_data('data_items','daily_yumi')
    json_items = json.loads(json_items)
    if request.method == 'POST':
        ymkqjc1 = request.form.get('ymkqjc1').split('+')
        ymkqjc2 = request.form.get('ymkqjc2').split('+')
        dfkqjc1 = request.form.get('dfkqjc1').split('+')
        dfkqjc2 = request.form.get('dfkqjc2').split('+')
        item['ymkqjc1'] = [ymkqjc1[0]+'+'+ymkqjc1[1],ymkqjc1[1]]
        item['ymkqjc2'] = [ymkqjc2[0]+'+'+ymkqjc2[1],ymkqjc2[1]]
        item['dfkqjc1'] = [dfkqjc1[0]+'+'+dfkqjc1[1],dfkqjc1[1]]
        item['dfkqjc2'] = [dfkqjc2[0]+'+'+dfkqjc2[1],dfkqjc2[1]]
        YuMi().run(ymkqjc1[0], ymkqjc2[0], dfkqjc1[0], dfkqjc2[0])
    print(item)
    return render_template('daily/yumi.html', item=item,today=today,content=content_item,items=json_items,val1=time.time())


# 股指信息
@app.route('/daily/guzhi',methods=['GET'])
@login_required
def guzhi():
    S= SelectDatas()
    content_item = S.select_data('content_items','daily_guzhi')
    content_item = json.loads(content_item)
    json_items = S.select_data('data_items','daily_guzhi')
    json_items = json.loads(json_items)
    today = str(datetime.datetime.today())[:10]
    return render_template('daily/guzhi.html', today=today,content=content_item,items=json_items,val1=time.time())

# 塑化信息
@app.route('/daily/shuhua',methods=['GET'])
@login_required
def shuhua():
    S= SelectDatas()
    content_item = S.select_data('content_items','daily_shuhua')
    content_item = json.loads(content_item)
    json_items = S.select_data('data_items','daily_shuhua')
    json_items = json.loads(json_items)
    today = str(datetime.datetime.today())[:10]
    return render_template('daily/shuhua.html',today=today,content=content_item,items=json_items,val1=time.time())

# 甲醇信息
@app.route('/daily/jiachun',methods=['GET'])
@login_required
def jiachun():
    S= SelectDatas()
    content_item = S.select_data('content_items','daily_jiachun')
    content_item = json.loads(content_item)
    json_items = S.select_data('data_items','daily_jiachun')
    json_items = json.loads(json_items)
    today = str(datetime.datetime.today())[:10]
    return render_template('daily/jiachun.html', items=json_items,content=content_item,today=today,val1=time.time())

# 橡胶信息
@app.route('/daily/xiangjiao',methods=['GET'])
@login_required
def xiangjiao():
    S= SelectDatas()
    content_item = S.select_data('content_items','daily_xiangjiao')
    content_item = json.loads(content_item)
    json_items = S.select_data('data_items','daily_xiangjiao')
    json_items = json.loads(json_items)
    today = str(datetime.datetime.today())[:10]
    return render_template('daily/xiangjiao.html',today=today,content=content_item,items=json_items,val1=time.time())


# 原油信息
@app.route('/daily/yuanyou',methods=['GET'])
@login_required
def yuanyou():
    S= SelectDatas()
    content1_item = S.select_data('content1_items','daily_yuanyou')
    content1_item = json.loads(content1_item)
    content2_item = S.select_data('content2_items','daily_yuanyou')
    content2_item = json.loads(content2_item)
    json_items = S.select_data('data_items','daily_yuanyou')
    json_items = json.loads(json_items)
    today = str(datetime.datetime.today())[:10]
    return render_template('daily/yuanyou.html',today=today,content1=content1_item,content2=content2_item,items=json_items,val1=time.time())

# PTA信息
@app.route('/daily/pta',methods=['GET'])
@login_required
def pta():
    S= SelectDatas()
    content_item = S.select_data('content_items','daily_pta')
    content_item = json.loads(content_item)
    json_items = S.select_data('data_items','daily_pta')
    json_items = json.loads(json_items)
    today = str(datetime.datetime.today())[:10]
    return render_template('daily/pta.html',today=today,content=content_item,items=json_items,val1=time.time())