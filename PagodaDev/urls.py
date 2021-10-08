"""PagodaDev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('article/', include('article.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog import views  # 导入blog应用views文件
from django.conf.urls import url

# 存放映射关系的列表
urlpatterns = [
    path(r'admin/', admin.site.urls),
    # path(r'register/', views.user_register),
    # path(r'login/', views.user_login),
    # url(r'^(\d+)/(\d+)/$', views.detail),
    # url(r'^(?P<category_id>\d+)/(?P<book_id>\d+)/$', views.detail),
    path(r'smsCode/', views.smsCode),
    path(r'add/', views.add),
    # blog应用的路由
    path(r'article/', include('blog.urls', namespace='article')),

    path(r'likes/', include('likes.urls', namespace='likes')),
    # 个人中心应用
    path(r'userprofile/', include('userprofile.urls', namespace='userprofile')),
    # 小工具应用
    path(r'miniTool/', include('miniTool.urls', namespace='miniTool')),

]
