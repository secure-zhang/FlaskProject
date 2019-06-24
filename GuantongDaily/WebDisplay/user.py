# -*- coding: utf-8 -*-

from __init__ import app,login_user, login_required,login_manager,logout_user
from flask import render_template,redirect,url_for,session,flash,request
from form import LoginForm,RegisterForm
from model import User
from datetime import timedelta
import time

# 创建user蓝图
from flask import Blueprint
user = Blueprint('user',__name__)


# 这个callback函数用于reload User object，根据session中存储的user id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 登出
@app.route('/logout')
def logout():
    logout_user()
    session.pop('username',None)
    session.pop('user_id',None)
    return redirect(url_for('index'))

# 登录
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        # 验证密码是否正确
        u = User.query.filter_by(email=data['email']).first()

        if u and u.check_password_hash(data['password']):
            if u.role:
                login_user(u)
                session['username'] = u.username
                session.permanent = True
                app.permanent_session_lifetime = timedelta(minutes=30)
                # 登录后重定向到之前的页面，url后缀即为函数名称，因此可以使用url_for
                # next = request.args.get('next')

                return redirect( url_for('index'))
            else:
                flash(u'请联系管理员开通权限')
        else:
            flash(u'密码无效')
    return render_template('login.html',form=form)

# 注册
@app.route('/register',methods=['GET','POST'])
def register():
        form = RegisterForm()
        if form.validate_on_submit():
            data = form.data
            # 写入用户信息
            u = User(username=data['username'],email=data['email'], password=data['password'])
            tag = u.add()
            if not tag:
                flash(u'注册失败,请重试')
                return redirect(url_for('register'))
            flash(u'注册成功,请登录')
            return redirect(url_for('login'))
        return render_template('register.html',form=form)
