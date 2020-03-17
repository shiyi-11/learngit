# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
#
# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
#
# app = Celery('celery',broker='redis://localhost:6379/1')
#
# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()
#
# # #
# # @app.task(bind=True)
# # def debug_task(self):
# #     print('Request: {0!r}'.format(self.request))















import os
from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MediaApp.settings')

# #Celery的参数是你当前项目的名称
# app = Celery('MediaApp')
#
# #这一步让你可以在django的settings.py中配置celery
# app.config_from_object('django.conf:settings')
#
# #celery会自动在你注册的app中寻找tasks.py，所以你的tasks.py必须放在各个app的目录下并且不能随意命名
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
# #这步暂时还不懂在做什么
# @app.task(bind=True)
# def test(self):
#     print('Request:{0!r}'.format(self.request))

