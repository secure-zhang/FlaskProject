# -*- coding: utf-8 -*-
# 发送邮件
from __init__ import app
from flask_mail import Mail, Message
from threading import Thread
from flask_login import login_required
from flask import Blueprint,request,render_template,flash,session
from form import EmailForm
send_emails = Blueprint('send_emails',__name__)
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '951428148@qq.com'
app.config['MAIL_PASSWORD'] = 'sjdfwqwdukfhbdii'
mail = Mail(app)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

@app.route('/send_email',methods=['GET','POST'])
@login_required
def send_email():
    form = EmailForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return
        username = session.get('username','null')
        title = form.title.data
        content = form.content.data
        new_title = '%s--%s'%(username,title)
        msg = Message(new_title, sender='951428148@qq.com', recipients=['17635035787@163.com'])
        msg.body = content
        flash('发送成功！')
        thread = Thread(target=send_async_email, args=[app, msg])
        thread.start()

    return render_template('datas/send_email.html',form=form)
