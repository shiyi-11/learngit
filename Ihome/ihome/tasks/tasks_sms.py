# coding:utf-8

from celery import Celery
from ihome.libs.yuntongxun.SendSMS import CCP

# 定义celery对象
celery_app = Celery('ihome',broker='redis://127.0.0.1:6379/1')

@celery_app.task
def sends_sms(to,datas,tempid):
	'''发送短信异步任务'''
	ccp = CCP()
	print('发送异步信息')

	ccp.send_sms(to,datas,tempid)
