# -*- coding: utf-8 -*-
# CreateTime: 2021/4/17 13:04

from django.conf.urls import url, include
from miniTool import views
from django.urls import path, re_path

# 需要执行app的名称
app_name = 'miniTool'

urlpatterns = [
    path('index/', views.query_member_price, name='index'),
]
