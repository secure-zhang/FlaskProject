# -*- coding: utf-8 -*-

from __init__ import app,login_user, login_required,login_manager,logout_user
from flask import render_template,session

# 首页
@app.route('/',methods=['GET','POST'])
def index():
    username = session.get('username',None)
    return render_template('index.html',username=username)


# 测试
@app.route('/test',methods=['GET','POST'])
def test():
    return render_template('test.html')


# 异常处理
@app.errorhandler(404)
def not_found(e):
    return render_template('error.html')

if __name__ == '__main__':
    # app.run(host='0.0.0.0',port=8000)
    app.run()
