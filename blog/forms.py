# -*- coding: utf-8 -*-
# CreateTime: 2021/5/22 12:22
# 引入表单类
from django import forms
# 引入文章类型
from blog import models


# 写文章的表单类
class ArticlePostForm(forms.ModelForm):
    """文章表单"""
    class Meta:
        # 指定数据的模型来源
        model = models.ArticlePost
        fields = ('title', 'body')  # 表单提交需要校验的字段


class CommentForm(forms.ModelForm):
    """评论表单"""
    class Meta:
        model = models.Comment
        fields = ['content']  # 表单提交需要校验的字段
