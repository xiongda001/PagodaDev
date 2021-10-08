# -*- coding: utf-8 -*-
# CreateTime: 2021/7/17 23:09

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect

# 配置需要走中间件校验的路由
loginRequired_list = ['/userprofile/personal_center', ]


class LoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # print('-----process_request')
        print(request.path)
        # 判断用户请求的路由是否在登录请求列表页
        if request.path in loginRequired_list:
            username = request.session.get('username')
            # 如果没有用户名则判定为未登录即跳转至登录页面
            if not username:
                return render(request, 'userprofile/login.html')

