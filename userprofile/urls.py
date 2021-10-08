# -*- coding: utf-8 -*-
# CreateTime: 2021/6/12 13:33

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from userprofile import views
from django.urls import path

# 需要执行app的名称
app_name = 'userprofile'

urlpatterns = [
    # url(r'', views.index, name='index'),
    path('register/', views.user_register, name='user_register'),
    path('check_user/', views.check_user, name='check_user'),  # 注册功能，检查用户是否可用的路由
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('user_center/<int:uid>', views.user_center, name='user_center'),  # 个人中心的路由
    path('user_center_edit/', views.user_center_edit, name='user_center_edit'),  # 编辑个人中心的路由
    # path('edit/<int:id>/', views.profile_edit, name='edit'),
    # path('register_ajax/', views.user_register),
    path('modify_icon/', views.modify_icon, name='modify_icon'),  # 修改头像的路由
    # path('search/', views.search, name='search'),  # AJAX搜索用户视图
    path('user_list/', views.user_list, name='user_list'),
    path('follow_user/<int:follow_user_id>', views.follow_user, name='follow_user'),
    path('ajax_add/', views.ajax_add),
    path('ajax_demo/', views.ajax_demo1),
    path('read_parent_index/<int:author_id>', views.read_parent_index, name='read_parent_index'),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

