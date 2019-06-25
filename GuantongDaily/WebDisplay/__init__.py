from flask import Flask
from flask_wtf.csrf import CsrfProtect
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

# app.debug=True
app.config["SECRET_KEY"] = "rootzhang"
app.secret_key = os.urandom(24)

# 指定数据库的链接信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://zhang:zhang@94.191.80.61:3306/Flask'
# 这个配置将来会被禁用,设置为True或者False可以解除警告信息,建议设置False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# csrf protection
csrf = CsrfProtect()
csrf.init_app(app)

# 用户登录模块
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user

# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message = u""
login_manager.init_app(app=app)




# 绑定蓝图
from daily import daily
from user import user
from datas import datas
from send_email import send_emails
app.register_blueprint(daily,url_prefix='/daily')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(datas, url_prefix='/datas')
app.register_blueprint(send_emails, url_prefix='/send_emails')
