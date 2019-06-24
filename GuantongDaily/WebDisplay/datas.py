# -*- coding: utf-8 -*-
# 数据页面

from __init__ import app
from flask import render_template,request,redirect,url_for,session
from flask_login import login_required
from mysql_db import SelectDatas
# 绑定datas蓝图
from flask import Blueprint
datas = Blueprint('datas',__name__)

# 持仓与成交
@app.route('/cjcc',methods=['GET'])
@login_required
def cjcc():
    num,result = SelectDatas().select_cjcc()
    return render_template('datas/cjcc.html',result=result,num=num)
