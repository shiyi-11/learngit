from django.core.mail import send_mail
from django.conf import settings
from celery import Celery
import time

import os
import django
# os.environ.setdefault('DJANGO_SETTING_MODULE', 'dailyfresh.setting')
os.environ['DJANGO_SETTINGS_MODULE'] = 'dailyfresh.settings'
django.setup()

app = Celery('celery_tasks.tasks', broker='redis://localhost/3')

@app.task
def send_register_email(username, token, email):
    message = ''
    title = '天天生鲜欢迎信息'
    body = '<h1>{name}，欢迎成为天天生鲜会员</h1>请点击下面链接激活账号<a href="http://127.0.0.1:8000/user/register/active/{token}">http://127.0.0.1:8000/user/register/active/{token}</a>'.format(
        name=username, token=token)
    try:
        send_mail(title, message, settings.EMAIL_FROM, [email], html_message=body)
    except Exception as e:
        pass

# from celery import shared_task
#
# @shared_task
@app.task
def test():
    for i in range(10):
        print('the test function is success {}'.format(i))
        time.sleep(1)

test.delay()
print()