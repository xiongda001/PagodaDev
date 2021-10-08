from datetime import datetime
from django.db import models
# from blog.models import ArticlePost
# from django.contrib.auth.models import User
# 引入内置信号
from django.db.models.signals import post_save
# 引入信号接收器的装饰器
from django.dispatch import receiver

# Create your models here.


class UserInfo(models.Model):
    """用户信息表"""
    username = models.CharField(max_length=12, unique=True, null=False, verbose_name='用户名', error_messages={'unique': '用户名必须唯一'})
    password = models.CharField(max_length=100, null=False, verbose_name='密码')
    age = models.IntegerField(null=True, verbose_name='年龄')
    confirm_password = models.CharField(max_length=100, null=False, verbose_name='确认密码')
    email = models.EmailField(verbose_name='邮箱')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    def __str__(self):
        return self.username

    class Meta:
        # 声明表名
        db_table = 'user'
        ordering = ('username', 'email')


class UserProfile(models.Model):
    """个人中心表"""
    # 与UserInfo够构成一对一的关系
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE, related_name='user_center')
    phone = models.CharField(max_length=11, blank=True, verbose_name='电话号码')
    icon = models.ImageField(upload_to='profile/%Y%m%d/', blank=True, null=True, verbose_name='头像')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    micro_blog = models.CharField(max_length=500, blank=True, verbose_name='微博地址')

    def __str__(self):
        return self.user.username

    class Meta:
        # 定义数据库中的表名
        db_table = 'profile'
        ordering = ('user', 'phone', 'icon')


class FollowUser(models.Model):
    """喜欢的用户表"""
    # 与UserInfo够构成一对一的关系
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='userinfo', verbose_name='喜欢的用户')
    source = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='添加来源')
    created = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        # 定义数据库中的表名
        db_table = 'followuser'

