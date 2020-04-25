# coding:utf-8

from celery import Celery
from ihome.tasks import config
# 定义celery对象
celery_app = Celery('ihome')
# 引入配置文件
celery_app.config_from_object(config)
# celery自动寻找任务
celery_app.autodiscover_tasks(["ihome.tasks.sms"])