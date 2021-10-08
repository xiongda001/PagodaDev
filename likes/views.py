from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, JsonResponse
from django.db.models import F  # F方法实现加1的功能
import json
from django.db.models import ObjectDoesNotExist
# from .models import LikeCount, LikeRecord
from django.contrib.auth.models import User
from blog.models import ArticlePost, Tag, Category, Comment


# def success_resp(liked_num):
#     """点赞成功响应体"""
#     data = {}
#     data['status'] = 'SUCCESS'
#     data['liked_num'] = liked_num
#     return JsonResponse(data)
#
#
# def error_resp(code, message):
#     """点赞失败相应码"""
#     data = {}
#     data['status'] = 'ERROR'
#     data['code'] = code
#     data['message'] = message
#     return JsonResponse(data)


# def like_change(request):
#     """获取数据"""
#
#     user = request.user
#     # 判断用户是否登录
#     if not user.is_authenticated:
#         return error_resp(40004, 'you were not login')
#
#     content_type = request.GET.get('content_type')
#     object_id = int(request.GET.get('object_id'))
#     # try:
#     content_type = ContentType.objects.get(model=content_type)
#     model_class = content_type.model_class()
#     model_obj = model_class.objects.get(pk=object_id)
#     print(f'model_obj是：{model_obj}')
#     # except ObjectDoesNotExist:
#     #     return error_resp(401, 'object not exist')
#
#     # 定义点赞上是否为True
#     # is_like = request.GET.get('is_like')
#     is_down = request.GET.get('is_down')
#
#     # 处理数据
#     if request.GET.get('is_like') == 'true':
#         # 进行点赞
#         like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id,
#                                                                 user=user)
#         if created:
#             # 未点过赞，进行点赞
#             like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
#             like_count.liked_num += 1
#             like_count.save()
#             return success_resp(like_count.liked_num)
#
#         else:
#             # 已点过赞，不能重复点赞
#             return error_resp(4001, "you were liked")
#
#     else:
#         # 取消点赞
#         if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
#             # 有点过赞，取消点赞
#             like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
#             like_record.delete()
#             # 点赞数量减1
#             like_count, created = LikeCount.objects.get_or_create(content_type, object_id=object_id)
#             if not created:
#                 like_count.liked_num -= 1
#                 like_count.save()
#                 return success_resp(like_count.liked_num)
#             else:
#                 return error_resp(4003, "data error")
#         else:
#             # 没有点赞过，不能取消
#             return error_resp(4002, "you were not liked")


# def up_down(request):
#     article_id = request.POST.get('article_id')
#     is_up = json.loads(request.POST.get('is_up'))  # 反序列化成为布尔值
#
#     # 点赞人即当前登陆人
#     user_id = request.user.pk
#
#     response = {'status': True, 'msg': None}
#
#     ard = LikeRecord.objects.create(user_id=user_id, article_id=article_id, is_up=True)
#     # 生成了赞记录， 然后再来更新页面
#     if is_up:  # 如果是赞就更新赞
#         LikeRecord.objects.filter(pk=article_id).update(up_count=F('up_count') + 1)
#     else:
#         # 踩的时候
#         ArticlePost.objects.filter(pk=article_id).update(down_count=F('down_count') + 1)
#     else:
#         response['state'] = False
#         response['handled'] = obj.is_up  # 将已经做过的操作提示
#
#
#     return JsonResponse(response)  # 必须用json返回
