# -*- coding: utf-8 -*-

from __init__ import app,login_user, login_required,login_manager,logout_user
from flask import render_template,session
from gevent.pywsgi import WSGIServer


# 首页
@app.route('/',methods=['GET','POST'])
@login_required
def index():
    username = session.get('username',None)
    return render_template('index.html',username=username)


# 测试
@app.route('/test',methods=['GET','POST'])
@login_required

def test():
    return render_template('test.html')


# 异常处理
@app.errorhandler(500)
@app.errorhandler(404)
@login_required
def not_found(e):
    return render_template('error.html')

if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 5000), app)
    # http_server = WSGIServer(('0.0.0.0', 8000), app)
    http_server.serve_forever()