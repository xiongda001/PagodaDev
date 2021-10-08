# -*- coding: utf-8 -*-
# CreateTime: 2021/4/17 13:04


from django.conf.urls import url, include
from blog import views
from django.urls import path, re_path

# 需要执行app的名称
app_name = 'blog'

urlpatterns = [
    path('index/', views.index, name='article_index'),
    path('article-create/', views.article_create, name='article_create'),
    path('article-list/', views.article_list, name='article_list'),

    # 参数id是取出id值相符合的唯一的一篇文章
    path('article-detail/<int:id>', views.article_detail, name='article_detail'),
    path('article-update/<int:id>', views.article_update, name='article_update'),
    path('article-delete/<int:id>', views.article_delete, name='article_delete'),
    # path('article-likeChange/<int:id>/', views.article_like_change, name='article_like_change'),
    path('article-like/<int:id>/', views.article_like, name='article_like'),
    path('article-dislike/<int:id>/', views.article_dislike, name='article_dislike'),

    path('comment/<int:article_id>', views.comment, name='comment'),
    # path('like/', views.like, name='like'),
    path('article_up_down/<int:article_id>', views.article_up_down, name='article_up_down'),
    path('comment_up_down/<int:comment_id>', views.comment_up_down, name='comment_up_down'),
]
