# 导入内建的User模型
from django.db import models
from datetime import datetime


from blog.models import ArticlePost, Comment
from userprofile.models import UserInfo


class UpDown(models.Model):
    """赞和踩"""
    article = models.ForeignKey(to=ArticlePost, null=True, on_delete=models.CASCADE, verbose_name='操作文章')
    comment = models.ForeignKey(to=Comment, null=True, on_delete=models.CASCADE, verbose_name='操作评论')
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE, verbose_name='赞踩者')
    is_up = models.CharField(max_length=100, verbose_name='赞踩状态')
    created = models.DateTimeField(default=datetime.now, verbose_name='赞踩时间')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '评价表'
        db_table = 'updown'

