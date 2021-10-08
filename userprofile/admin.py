from django.contrib import admin

# Register your models here.
from userprofile.models import UserInfo, UserProfile


# 注册ArticlePost到admin中
admin.site.register(UserInfo)
admin.site.register(UserProfile)
