# -*- coding: utf-8 -*-
# CreateTime: 2021/6/12 12:55

# 引入表单类
from django import forms
# 引入User模型
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo
from django.contrib.auth.forms import UserCreationForm


# 登录表单，继承了forms.Form类
class UserLoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密码', min_length=8)


# 用户注册表单类
class UserRegisterForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password1 = forms.CharField(label='密码', min_length=8)
    password2 = forms.CharField(label='确认密码', min_length=8)

    # 添加email到默认的UserCreationForm
    email = forms.EmailField(label='电子邮件')

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码是否一致进行检查
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password1') == data.get('password2'):
            return data.get('password1')
        else:
            raise forms.ValidationError('密码输入不一致，请重新输入')


class UserProfileForm(forms.ModelForm):
    class Meta:
        # 指定数据的模型来源
        model = UserProfile
        fields = ('phone', 'icon', 'bio', 'micro_blog')  # 表单提交需要校验的字段


class UserInfoForm(forms.ModelForm):
    class Meta:
        # 指定数据的模型来源
        model = UserInfo
        fields = ('username',)  # 表单提交需要校验的字段
