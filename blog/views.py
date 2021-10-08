import json
import re
import string
import random
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, render_to_response
from django.template import Template, Context
from django.core.cache import cache
from django import forms
import requests
import time
from blog.models import ArticlePost, Tag, Category, Comment
from likes.models import UpDown
from userprofile.models import UserInfo, UserProfile
from userprofile.views import *
from django.contrib.auth.models import User
from django.urls import reverse
from blog.forms import ArticlePostForm, CommentForm
from django.core.paginator import Paginator
from django.db.models import Q, F  # Q方法实现搜索功能
from django.contrib.auth.decorators import login_required


def random_data():
    """随机返回4位数字"""
    seeds = string.digits
    random_str = random.sample(seeds, k=4)
    return (''.join(random_str))


# def user_register(request):
#     """注册"""
#     resp = [
#         {'statusCode': 10001, 'message': '不支持该请求方法'},
#         {'statusCode': 10002, 'message': '手机号必须为11位'},
#         {'statusCode': 10003, 'message': '手机号不能为空'},
#         {'statusCode': 0, 'SMSCode': random_data()}
#     ]
#     if request.method == 'GET':
#         """返回注册页面"""
#         return render(request, 'register.html')
#     else:
#         phoneNum = request.POST.get('phoneNumber')
#         if len(phoneNum) != 11:
#             return JsonResponse(resp[1], json_dumps_params={'ensure_ascii': False})
#         else:
#             return JsonResponse(resp[-1])
#
#
# def user_login(request):
#     """登录"""
#     resp = [
#         {'statusCode': 10001, 'message': '用户名或密码错误'},
#         {'statusCode': 0, 'message': '登录成功'}
#     ]
#     if request.method == 'GET':
#         """返回注册页面"""
#         return render(request, 'login.html')
#     else:
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         if username == 'admin' and password == '123456':
#             return JsonResponse(resp[-1], json_dumps_params={'ensure_ascii': False})
#         else:
#             return JsonResponse(resp[0], json_dumps_params={'ensure_ascii': False})


def get_sms_code(phoneNum, startTime=int(time.time()), endTime=int(time.time()) * 1000):
    """发送短信验证码后端接口"""
    base_url = 'http://139.199.224.115:9016/'
    headers = {
        "authToken": "A897EE539B5C3221A73B768E63989DD28BCCEF36BFC67B79EB8FFCACA21B8245E2F481DCA78C6D209138119903D2FBE3"}
    api_url = 'smsgateway/smsService/getSmsReport'
    lastId = '190737501'
    # startTime = int(time.time())
    # print(startTime)
    # endTime = int(time.time()) * 1000
    # print(endTime)
    data = {'lastId': lastId, 'phoneNum': phoneNum, 'startTime': startTime, 'endTime': endTime}
    url = base_url + api_url
    # 发送请求
    resp = requests.post(url=url, data=data, headers=headers)
    print(f'返回的对象类型{type(resp.text)}')
    return resp.text


def smsCode(request):
    """获取短信验证码"""
    phoneNum = request.POST.get("mobile")
    startTime = 1620645504
    endTime = request.POST.get("endTime")

    # 参数化获取短信验证码
    resp_text = get_sms_code(phoneNum, startTime=startTime, endTime=int(time.time()) * 1000)
    resp_text_list = json.loads(resp_text)  # json字符串转换成python字典对象

    # print(resp_text_list)

    if request.method == 'get':
        return render(request, 'homePage.html')
    else:
        # 获取前端输入的手机号
        phoneNum = request.POST.get("mobile")
        print(f'手机号：{phoneNum}')
        # if len(phoneNum) != 11:
        #     return render(request, 'sendSMSCode.html', {'sms_code': '请输入11位手机号'})

        startTime = 1620645504
        endTime = request.POST.get("endTime")
        # 获取选择环境元素的值
        select_op = request.POST.get("select_op")
        print(f'环境选择：{select_op}')

        content_list = []  # 把遍历出来的数据添加到新列表
        for index_dict in resp_text_list:
            print(f'索引：{index_dict}')
            smsContent = index_dict.get('smsContent')  # 遍历验证码内容
            # print(f'验证码的内容：{smsContent}')
            # print('-----' * 8)
            # print(resp_text_list)
            content_list.append(smsContent)

        code_list = content_list[1:-1]  # 切片只获取有登录验证码的内容
        # 截取4位数验证码
        print(f'登录验证码的短信：{code_list}')

        code_list = re.findall('\d{4}', str(code_list))
        print(f'正则匹配的4位数数组：{code_list}')

        code_content_list = []  # 创建获取验证码后的list
        for code in code_list:
            if select_op == "1":
                # TEST环境返回的验证码
                test_env_code = "1" + code
                # 设置前端返回的内容
                code_content = f'{phoneNum} 手机号获取的验证码是：{test_env_code}'
                code_content_list.append(code_content)
                # return render(request, 'sendSMSCode.html', context={'sms_code': test_env_code})

            elif select_op == "2":
                # UAT环境返回的验证码
                uat_env_code = "2" + code
                # 设置前端返回的内容
                code_content = f'{phoneNum} 手机号获取的验证码是：{uat_env_code}'
                code_content_list.append(code_content)
                # return render(request, 'sendSMSCode.html', context={'sms_code': uat_env_code})

            elif select_op == "3":
                # 生产环境返回的验证码
                prod_env_code = "3" + code
                # 设置前端返回的内容
                code_content = f'{phoneNum} 手机号获取的验证码是：{prod_env_code}'
                code_content_list.append(code_content)

                # return render(request, 'sendSMSCode.html', context={'sms_code': prod_env_code})
        print('*****' * 5)
        print(f'最终的验证码列表：{code_content_list}')
    return render(request, 'sendSMSCode.html', context={'sms_code': code_content_list})


# 新增一个帖子
def add(request):
    article_title = request.POST.get('article_title', "")
    article_prief = request.POST.get('article_prief', "")
    article_content = request.POST.get('article_content', "")
    # add_article=Article(article_title=article_title,article_prief_content=article_prief,article_content=article_content);
    # add_article.save();

    return render(request, 'form_demo.html', {
        'article_title': article_title,
        'article_prief': article_prief,
        'article_content': article_content,
    })


def index(request):
    """博客首页"""
    post_list = ArticlePost.objects.all()
    context = {'title': '我的博客首页',
               'welcome': '欢迎，大佬！'}
    return render(request, 'index.html', context={'post_list': post_list})


def login_decorator(func):
    """登录装饰器"""

    def inner(request, *args, **kwargs):
        ret = request.session.get('is_login')
        if ret == 1:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'userprofile/login.html')

    return inner


def article_create(request):
    """创建文章"""
    login_status = request.session.get('is_login')
    login_user = request.session.get('username')
    if not login_status:
        return redirect('userprofile:user_login')

    login_user_id = UserInfo.objects.get(username=login_user).id
    logger.info(f'article_create页拿到当前登录的信息: {login_user_id},{login_user}')

    if request.method == 'POST':
        blog_title = request.POST.get('title')
        blog_body = request.POST.get('body')

        # 获取用户id
        user_id = UserInfo.objects.get(username=login_user).id

        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            # new_article = article_post_form.save(commit=False)

            # 创建文章
            new_article = ArticlePost.objects.create(title=blog_title, body=blog_body, author_id=user_id)
            # new_article.author = ArticlePost.objects.filter(author='zhangsan').first()
            print(f'文章作者：{new_article.author}')

            # 将文章保存到数据库中
            # new_article.save()
            return redirect('article:article_list')
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse('表单内容有误，请重新编写')
    # 如果用户请求获取数据
    else:
        # 创建表单实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form': article_post_form}
        # 返回模板
        return render(request, 'article/create.html', context)


def article_list(request):
    """文章列表"""
    login_status = request.session.get('is_login')
    login_user = request.session.get('username')
    if not login_status:
        return redirect('userprofile:user_login')

    login_user_id = UserInfo.objects.get(username=login_user).id
    logger.info(f'article_list页拿到当前登录的信息: {login_user_id},{login_user}')

    search = request.GET.get('search')
    logger.info(f'search的内容：{search}')
    # order = request.GET.get('order')
    # logger.info(f'order的内容：{order}')
    # 文章搜索
    if search:
        logger.info(f'search的内容：{search}')
        if search == 'total_views':
            # Q(title__icontains)意思是用模型的title字段查询，中间用两个下划线隔开，icontaions中的i是不区分大小写
            # search是需要查询的文本。& 代表与逻辑，| 代表或逻辑，~ 代表非逻辑
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) | Q(body__icontains=search) | Q(author__username__icontains=search)).order_dy('-total_views')
        else:
            article_list = ArticlePost.objects.filter(Q(title__icontains=search) | Q(body__icontains=search) | Q(author__username__icontains=search))

    else:
        # 将search参数重置为空
        search = ''
        """
        # 为什么需要search = ''语句？如果用户没有搜索操作，则search = request.GET.get('search')会使得search = None，
        # 而这个值传递到模板中会错误地转换成"None"字符串！等同于用户在搜索“None”关键字，这明显是错误的
        """
        if search == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
            # article_list = ArticlePost.objects.get(author=user).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()
            # article_list = ArticlePost.objects.get(author=user)

    # 分页功能：取出所有博客文章
    # article_list = ArticlePost.objects.all()

    # 定义每页显示6篇文章
    paginator = Paginator(article_list, 6)
    # 获取url中的页码
    page = request.GET.get('page')
    logger.info(f'page的内容是: {page}')
    # 将导航对象相应的页码内容返回给articles
    articles = paginator.get_page(page)

    # 增加search到context
    context = {'articles': articles,  'search': search, 'user': login_user, 'login_user_id': login_user_id}
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    """文章详情"""
    login_status = request.session.get('is_login')
    login_user = request.session.get('username')
    if not login_status:
        return redirect('userprofile:user_login')

    login_user_id = UserInfo.objects.get(username=login_user).id
    logger.info(f'article_detail页拿到当前登录的信息login_user_id：{login_user_id},login_user：{login_user}')
    # if not status:
    #     return redirect('userprofile:user_login')

    # 取出id值相符合的唯一的一篇文章
    article = ArticlePost.objects.get(pk=id)
    print(f'article_detail视图输出的值：{article.id}')
    # 取出文章评论
    comments = Comment.objects.filter(article=id)

    # 添加comments上下文
    return render(request, 'article/detail.html', {'article': article, 'comments': comments, 'user': login_user})


def article_delete(request, id):
    """删除文章"""
    # 根据id获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 删除文章
    article.delete()
    # 执行删除后返回文章列表页(指定的参数是blog，其他函数调用的是article)
    return redirect('blog:article_list')


def article_update(request, id):
    """
    修改文章
    通过post方法提交表单，更新title、body字段
    get方法进入初始表单页面
    id：文章的id
    """
    # 获取需要修改的文章对象
    article = ArticlePost.objects.get(id=id)
    print(article)

    # 判断用户是否为post提交表单数据
    if request.method == 'POST':

        # 将提交的表单赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)

        # 判断用户提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的title、body内容
            article.title = request.POST.get('title')
            article.body = request.POST.get('body')
            article.save()

            # 完成后返回到修改的文章，需传入文章的id值
            url = redirect('article:article_detail', id=id)
            print(f'请求的url地址：{url}')
            return url

        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse('表单内容有误，请重新填写')

    # 如果用户get请求获取数据，
    else:
        # 创建表单实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将article文章对象也传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form}
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


def article_like(request, id):
    """文章点赞-无限赞"""
    receive_id = id
    # print(receive_id)
    data = {}  # 返回json信息
    # 查询该id对应的文章
    article = ArticlePost.objects.defer('body').get(id=receive_id)
    # 点赞数+1
    article.like += 1
    print(f'ID为{receive_id}的文章点赞总数是：{article.like}')
    article.save()

    # 定义ajax请求成功后返回的响应内容
    data['like_' + str(receive_id)] = article.like
    print(data)

    return JsonResponse(data)


def article_dislike(request, id):
    """文章点踩-无限踩"""
    receive_id = id
    # print(receive_id)
    data = {}  # 返回json信息
    # 查询该id对应的文章
    article = ArticlePost.objects.defer('body').get(id=receive_id)
    # 点踩数+1
    article.dislike += 1
    print(f'ID为{receive_id}的文章点踩总数是：{article.dislike}')
    article.save()

    # 定义ajax请求成功后返回的响应内容
    data['dislike_' + str(receive_id)] = article.dislike

    return JsonResponse(data)


def comment(request, article_id):
    """文章评论"""
    status = request.session.get('is_login')
    user = request.session.get('username')
    logger.info(f'文章评论拿到的用户信息是: {status},{user}')
    if not status:
        return redirect('userprofile:user_login')

    # 通过文章id获取文章对象
    comment_article = ArticlePost.objects.get(pk=article_id).id
    logger.info(f'comment_article的id是：{comment_article}')

    # 过滤评论的用户
    comment_user = UserInfo.objects.filter(username=user).first()
    logger.info(f'---comment_user---：{comment_user}')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            logger.info(f'---new_comment---：{new_comment}')
            # 文章id
            new_comment.article_id = comment_article
            # 文章评论者
            new_comment.user = comment_user
            comment_form.save()
            # 重定向到文章详情页
            return redirect(f'/article/article-detail/{article_id}')
            # return redirect('article:article_detail', article_id=comment_article)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        return HttpResponse("发表评论仅接受POST请求。")


def article_up_down(request, article_id):
    """文章的赞和踩"""
    login_status = request.session.get('is_login')
    user = request.session.get('username')
    print('----' * 10)
    print(type(user))
    logger.info(f'文章赞和踩: {login_status},{user}')

    # 获取用户id
    userId = UserInfo.objects.get(username=user).id
    logger.info(f'up_down视图函数的用户ID: {userId}')

    # 查询该id对应的文章对象
    articleId = ArticlePost.objects.get(pk=article_id).id
    # article_id = request.POST.get('article_id')
    logger.info(f'up_down函数中拿到的article是：{articleId}')

    isUp = request.POST.get("is_up")  # 前端ajax定义的入参的key名
    # is_up = json.loads(is_up)  # 前端数据默认以json传来，并转换成python字典对象布尔值
    logger.info(f'前端拿到的is_up：{isUp}')

    object = UpDown.objects.filter(article_id=articleId, user_id=userId).first()
    logger.info(f'正在操作的文章object是: {object}')

    # 定义回调参数
    send_info = {'object': None, 'is_up': None, 'handled': None, 'msg': None}
    if not object:

        # 用户初次点赞
        if isUp == 'up':
            # 往UpDown表里插入对象
            UpDown.objects.create(is_up=isUp, article_id=articleId, user_id=userId)
            # ArticlePost.objects.filter(pk=article_id).update(like=F('like') + 1)

            # 更新文章点赞数
            article = ArticlePost.objects.defer('body').get(pk=articleId)
            article.like += 1
            logger.info(f'ID为{articleId}的文章点赞总数是：{article.like}')
            article.save()

            send_info['object'] = False
            send_info['is_up'] = 'up'
            send_info['handled'] = 'up_first'
            send_info['msg'] = '支持一下'

        # 用户初次点踩
        else:
            # 往UpDown表里插入对象
            UpDown.objects.create(is_up='down', article_id=articleId, user_id=userId)

            # 更新文章点踩数
            ArticlePost.objects.filter(pk=articleId).update(dislike=F('dislike') + 1)
            send_info['object'] = False
            send_info['is_up'] = 'down'
            send_info['handled'] = 'down_first'
            send_info['msg'] = '吐槽一下'

    else:
        # 获取UpDown表中已有的对象记录
        handle_obj = UpDown.objects.get(user_id=userId, article_id=articleId)
        logger.info(f'操作的文章handle_obj: {handle_obj}')

        # 获取upDown表中记录is_up=up 时
        if handle_obj.is_up == 'up':

            # 用户重复点赞
            if isUp == 'up':
                # send_info['article_id'] = articleId
                send_info['object'] = True
                send_info['is_up'] = 'up'
                send_info['handled'] = 'up_double'
                send_info['msg'] = '您已经支持过了哦~~~'

            # 用户点击踩，则文章的踩数量+1、赞数量-1 并更新updown表中is_up字段值
            else:
                UpDown.objects.filter(user_id=userId, article_id=articleId).update(is_up='down')

                ArticlePost.objects.filter(pk=article_id).update(dislike=F('dislike') + 1)
                ArticlePost.objects.filter(pk=article_id).update(like=F('like') - 1)

                send_info['object'] = True
                send_info['is_up'] = 'down'
                send_info['handled'] = 'up_to_down'
                send_info['msg'] = '由支持变成吐槽'

        # 获取upDown表中记录is_up=down 时
        else:
            # 用户重复点踩
            if isUp == 'down':
                # send_info['article_id'] = articleId
                send_info['object'] = True
                send_info['is_up'] = 'down'
                send_info['handled'] = 'down_double'
                send_info['msg'] = '您已经吐槽过了哦~~~'

            # 用户点击赞，则文章的赞数量+1、踩数量-1 并更新updown表中is_up字段值
            else:
                UpDown.objects.filter(user_id=userId, article_id=articleId).update(is_up='up')

                ArticlePost.objects.filter(pk=article_id).update(like=F('like') + 1)
                ArticlePost.objects.filter(pk=article_id).update(dislike=F('dislike') - 1)

                send_info['object'] = True
                send_info['is_up'] = 'up'
                send_info['handled'] = 'down_to_up'
                send_info['msg'] = '由吐槽变成支持'

    logger.info(f'send_info: {send_info}')

    return JsonResponse(send_info)


def comment_up_down(request, comment_id):
    """文章评论的赞和踩"""
    login_status = request.session.get('is_login')
    user = request.session.get('username')
    print('----' * 10)
    print(type(user))
    logger.info(f'文章评论赞和踩: {login_status},{user}')

    # 获取用户id
    userId = UserInfo.objects.get(username=user).id
    logger.info(f'comment_up_down视图函数拿到的用户ID是: {userId}')

    # 查询该id对应的文章对象
    # articleId = ArticlePost.objects.get(pk=article_id).id
    # # article_id = request.POST.get('article_id')
    # logger.info(f'comment_up_down拿到的commentId：{articleId}')

    # 评论id
    commentId = Comment.objects.get(pk=comment_id).id  # 前端ajax定义的入参的key名
    logger.info(f'comment_up_down拿到的commentId：{commentId}')

    # 点踩操作
    isUp = request.POST.get("is_up")  # 前端ajax定义的入参的key名
    logger.info(f'前端拿到的is_up：{isUp}')

    comment_object = UpDown.objects.filter(comment_id=commentId, user_id=userId).first()
    logger.info(f'正在操作的文章评论object: {comment_object}')

    # 定义响应参数
    send_info = {'comment_object': None, 'is_up': None, 'handled': None, 'msg': None}
    if not comment_object:

        # 初次点赞
        if isUp == 'up':
            # 往UpDown表里插入对象
            UpDown.objects.create(is_up=isUp, comment_id=commentId, user_id=userId)

            # 更新评论点赞数
            Comment.objects.filter(pk=commentId).update(like=F('like') + 1)
            logger.info(f'comment数据类型：{type(Comment)}')
            logger.info(f'ID为{commentId}的评论点赞总数是：{Comment.like}')

            send_info['comment_object'] = False
            send_info['is_up'] = 'up'
            send_info['handled'] = 'up_first'
            send_info['msg'] = '支持一下'

        # 初次点踩
        else:
            # 往UpDown表里插入对象
            UpDown.objects.create(is_up='down', comment_id=commentId, user_id=userId)

            # 更新评论点踩数
            comment = Comment.objects.filter(pk=commentId).update(dislike=F('dislike') + 1)
            logger.info(f'comment数据类型：{type(comment)}')
            logger.info(f'ID为{commentId}的评论吐槽总数是：{Comment.dislike}')

            send_info['comment_object'] = False
            send_info['is_up'] = 'down'
            send_info['handled'] = 'down_first'
            send_info['msg'] = '吐槽一下'

    else:
        # 获取UpDown表中已有的对象记录
        handle_obj = UpDown.objects.get(user_id=userId, comment_id=commentId)
        logger.info(f'操作的文章评论handle_obj: {handle_obj}')

        # 获取upDown表中记录is_up=up 时
        if handle_obj.is_up == 'up':

            # 用户重复点赞
            if isUp == 'up':

                send_info['comment_object'] = True
                send_info['is_up'] = 'up'
                send_info['handled'] = 'up_double'
                send_info['msg'] = '您已经支持过了哦~~~'

            # 用户点击踩，则评论的踩数量+1、赞数量-1 并更新updown表中is_up字段值
            else:
                UpDown.objects.filter(user_id=userId, comment_id=commentId).update(is_up='down')

                Comment.objects.filter(pk=commentId).update(dislike=F('dislike') + 1)
                Comment.objects.filter(pk=commentId).update(like=F('like') - 1)

                send_info['comment_object'] = True
                send_info['is_up'] = 'down'
                send_info['handled'] = 'up_to_down'
                send_info['msg'] = '由支持变成吐槽'

        # 获取upDown表中记录is_up=down 时
        else:
            # 用户重复点踩
            if isUp == 'down':

                send_info['comment_object'] = True
                send_info['is_up'] = 'down'
                send_info['handled'] = 'down_double'
                send_info['msg'] = '您已经吐槽过了哦~~~'

            # 用户点击赞，则评论的赞数量+1、踩数量-1 并更新updown表中is_up字段值
            else:
                UpDown.objects.filter(user_id=userId, comment_id=commentId).update(is_up='up')

                Comment.objects.filter(pk=commentId).update(like=F('like') + 1)
                Comment.objects.filter(pk=commentId).update(dislike=F('dislike') - 1)

                send_info['comment_object'] = True
                send_info['is_up'] = 'up'
                send_info['handled'] = 'down_to_up'
                send_info['msg'] = '由吐槽变成支持'

    logger.info(f'send_info: {send_info}')

    return JsonResponse(send_info)

