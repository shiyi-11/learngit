# coding:utf-8

from ihome.tasks.main import celery_app
from ihome.libs.yuntongxun.SendSMS import CCP

@celery_app.task
def sends_sms(to,datas,tempid):
	'''发送短信异步任务'''
	ccp = CCP()
	print('发送异步信息')

	res=ccp.send_sms(to,datas,tempid)

	return res