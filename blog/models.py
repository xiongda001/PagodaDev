# Create your models here.
from datetime import datetime
from django.db import models

# 处理时间相关事务
from django.utils import timezone
from userprofile.models import UserInfo
from django.urls import reverse


class Category(models.Model):
    """
    创建【分类】表，字段如下
    1.分类名称-name
    """

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    name = models.CharField(max_length=100)

    def __str__(self):
        # 将分类名称返回
        return self.name


class Tag(models.Model):
    """
    创建【标签】表，字段如下
    1.标签名称-name
    """
    name = models.CharField(max_length=100)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # 将标签名称返回
        return self.name


class ArticlePost(models.Model):
    """
    创建【文章】表，字段如下
    1.文章标题：title
    2.文章内容：body
    3.创建时间：created
    4.修改时间：updated
    5.作者：author
    """
    title = models.CharField(max_length=50)
    body = models.TextField()
    # 文章创建时间，创建数据时默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)
    # 文章更新时间，参数auto_now=True指定每次数据更新时自动写入当前的时间
    updated = models.DateTimeField(auto_now=True)
    # 文章作者与UserInfo表中的username进行关联，参数 on_delete 用于指定数据删除的方式，避免两个关联表的数据不一致
    author = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    # 点赞字段
    like = models.IntegerField(default=0)
    # 点踩字段
    dislike = models.IntegerField(default=0)

    class Meta:
        # ordering 指定模型返回的数据排序顺序, '-created' 表明数据应该以倒序排序
        ordering = ('-created',)
        db_table = 'article'

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # 将文章标题返回
        return self.title

    # def get_absolute_url(self):
    #     """获取文章地址"""
    #     return reverse('article:article_detail', args=[self.id])


class Comment(models.Model):
    """文章评论"""
    id = models.AutoField(primary_key=True, verbose_name='评论ID')
    # 被评论的文章，与ArticlePost文章表建立关联
    article = models.ForeignKey(to=ArticlePost, on_delete=models.CASCADE, verbose_name='文章')
    # 评论者，与UserInfo表建立关联
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE, verbose_name='评论者')
    content = models.TextField(verbose_name='评论内容')
    created = models.DateTimeField(default=datetime.now, verbose_name='评论时间')
    updated = models.DateTimeField(auto_now=True)
    # 点赞字段
    like = models.IntegerField(default=0)
    # 点踩字段
    dislike = models.IntegerField(default=0)

    class Meta:
        verbose_name = '文章评论'
        ordering = ('-created',)  # 按创建时间倒序
        db_table = 'comment'

    def __str__(self):
        return self.content[:20]

