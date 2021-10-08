from django.contrib import admin
from blog.models import ArticlePost, Comment
# Register your models here.

# 注册ArticlePost到admin中
admin.site.register(ArticlePost)

admin.site.register(Comment)
