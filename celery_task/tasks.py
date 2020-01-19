#使用celery
from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import time

#在任务处理者一端加上
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
django.setup()


# 创建Celery对象  路径        broker是 redis的8号库
app = Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379/8')

# 定义任务函数发邮件
#使用task  在视图函数中调用该方法
@app.task
def send_register_active_email(to_emali,username,token):
    '''发送激活邮件'''
    subject = '生鲜信息欢迎你'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_emali]
    html_message = '<h1>%s,欢迎您成为会员，</h1点击下链接激活用户</br><a href="http:127.0.0.1:8000/user/active/%s">http:127.0.0.1:8000/user/active/%s</a>' % (
    username, token, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)
    time.sleep(5)










