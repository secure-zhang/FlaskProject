# -*- coding: utf-8 -*-
#
from __init__ import db
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from flask_login._compat import unicode
from _datetime import datetime


class User(UserMixin,db.Model):
    __tablename__ = 'user'
    # 创建字段
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(64),nullable=False)
    email = db.Column(db.String(30), nullable=False,unique=True)
    password_hash = db.Column(db.String(256),nullable=False)
    register_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    role = db.Column(db.Boolean, default=False,nullable=False)

    def __str__(self):
        return 'User{username=%s,email=%s,password=%s,}' % (self.username, self.email, self.password,)

    @property
    def password(self):
        raise AttributeError('password is not readable')

    #密码设置为hash
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    #验证密码
    def check_password_hash(self,password):
        return check_password_hash(self.password_hash,password)


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return 1
        except:
            return 0

    def __repr__(self):
        return '<User %r>' % (self.name)


if __name__ == '__main__':
    db.create_all()
