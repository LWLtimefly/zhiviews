from __future__ import absolute_import   # 绝对路径导入

import os

# 设置系统环境  DJANGO_SETTINGS_MODULE
from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','BestJob.settings')

app = Celery('BestJob')

# 配置celery
app.config_from_object('django.conf:settings')

# 自动从当前项目已安装的app中查找task
app.autodiscover_tasks(lambda : settings.INSTALLED_APPS)

