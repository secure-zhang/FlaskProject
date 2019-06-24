# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField,TextAreaField,SubmitField,validators
from wtforms.validators import DataRequired,Length,EqualTo,Email
from model import User

class LoginForm(FlaskForm):
    # 用户登录表单
    email = StringField(label='邮箱',
                        validators=[Email(message='无效的邮箱格式'),DataRequired(message='邮箱不能为空')],
                        render_kw={
                            'class': 'form-email',
                            'placeholder': u'请输入邮箱'
                        })
    password = PasswordField(label='密码',
                             validators=[DataRequired(message='密码不能为空'), Length(6, 20, message='密码只能在6~20个字符之间')],
                             render_kw={
                                 'class': 'form-password',
                                 'placeholder': u'请输入密码'
                             }
                             )
    submit = SubmitField(label='登录',
                         render_kw={
                             'class': 'btn btn-default',
                            'placeholder': u'登录'
    }
                         )
    # 验证邮箱是否存在
    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise validators.StopValidation(u'邮箱未找到')

    # 验证密码
    # def validate_password(self, field):
    #     user = User.query.filter_by(email=self.email.data).first()
    #     if user:
    #         if not user.check_password_hash(field.data):
    #             raise validators.StopValidation(u'密码不正确')

class RegisterForm(FlaskForm):
    # 用户注册表单
    username = StringField(label='姓名',
                           validators=[DataRequired(message='姓名不能为空'), Length(2, 6, message='姓名只能在2~6个字符之间')],
                           render_kw={
                               'class': 'form-control',
                               'placeholder': u'请输入姓名'
                           }
                           )
    email = StringField(label='邮箱',
                        validators=[Email(message='无效的邮箱格式'),DataRequired(message='邮箱不能为空')],
                        render_kw={
                            'class': 'form-control',
                            'placeholder': u'请输入邮箱'
                        }
                        )
    password = PasswordField(label='密码',
                             validators=[DataRequired(message='密码不能为空'), Length(6, 20, message='密码只能在6~20个字符之间')],
                             render_kw={
                                 'class': 'form-control',
                                 'placeholder': u'请输入密码'
                             }
                             )
    confirm = PasswordField(label='确认密码',
                            validators=[EqualTo('password', message='两次密码不一致'),DataRequired(message='密码不能为空')],
                            render_kw={
                                'class': 'form-control',
                                'placeholder': u'请确认密码'
                            }
                            )
    submit = SubmitField(label='注册',
                         render_kw={
                             'class': 'btn btn-success',
                            'placeholder': u'注册'
    }
                         )

    # 验证邮箱是否存在
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise validators.StopValidation(u'该邮箱已注册使用，请选用其它邮箱')

class EmailForm(FlaskForm):
    # 发送邮件表单
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Contents', validators=[DataRequired()])
