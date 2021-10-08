import hashlib
import json
from loguru import logger
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password

from blog.models import ArticlePost
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm
from userprofile.models import UserInfo, UserProfile, FollowUser


def user_register(request):
    """用户注册"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # 定义错误信息
        context = [
            '两次密码不一致',
            '用户名或密码不能为空',
            '该用户名已注册'
        ]

        if username and password and confirm_password:
            # 判断两次密码是否相等
            if password == confirm_password:
                # 密码加密
                pwd = make_password(password=password)
                # 密码校验通过后则创建用户
                user = UserInfo.objects.create(username=username, password=pwd)
                print(f'注册页面拿到的user信息：{user}')
                # 注册成功后把用户信息写进UserProfile表中
                UserProfile.objects.create(user_id=user.id)
                user.save()

                # # 密码进行16进制加密
                # user.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                return redirect('article:article_list')

    return render(request, 'userprofile/register.html')


"""
def register_form(request):
    '''注册功能表单校验'''
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        print(f'用户注册表单: {user_register_form}')

        # 校验用户提交的数据是否满足模型的要求
        if user_register_form.is_valid():
            username = user_register_form.cleaned_data.get('username')
            filter_result = UserInfo.objects.filter(username=username)
            if (len(filter_result)) > 0:
                return render_to_response({'error': '用户名已存在'})

            else:
                password1 = user_register_form.cleaned_data['password1']
                password2 = user_register_form.cleaned_data['password2']
                errors = []
                if password1 != password2:
                    errors.append('两次输入的密码不一致！')
                    return render_to_response({'error': errors})
                else:
                    user = UserInfo.objects.create_user(username=username, password=password1)
                    user.save()
                    return redirect('article:article_list')

    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse('请使用GET或POST方法请求数据')
"""


def check_user(request):
    """检查注册时用户名是否有效"""
    username = request.GET.get('username')
    user = UserInfo.objects.filter(username=username).first()
    # 用户名不为空，查询数据库
    if user:
        logger.info(f'user：{user}')
        return JsonResponse({"status": "fail", "msg": "此用户名已占用"})
    else:
        return JsonResponse({"status": "success", "msg": "用户名可用"})


'''
def user_login(request):
    """登录的表单校验方法"""
    if request.method == 'POST':
        # 将提交的数据赋值到表单实例中
        user_login_form = UserLoginForm(data=request.POST)
        print(f'用户提交的表单数据：{user_login_form}')

        # 判断提交的数据是否满足模型要求
        if user_login_form.is_valid():
            #  .cleaned_data 清洗出合法数据
            data = user_login_form.cleaned_data
            print(f'打印登录用户{data}')

            # 检验账号、密码是否正确匹配数据库中的某个用户
            user = authenticate(username=data['username'], password=data['password'])
            print(f'user信息：{user}')
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request, user)
                # 登录成功后跳转至文章列表页
                return redirect('article:article_list')
            else:
                return JsonResponse({'status': 401, 'msg': '账号或密码输入有误'}, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse({'status': 402, 'msg': '账号或密码输入不合法'})

    return render(request, 'userprofile/login.html')
'''


def user_login(request):
    """用户登录"""
    if request.method == 'POST':
        user_name = request.POST.get('username')
        user_pwd = request.POST.get('password')
        # 获取用户信息
        user_obj = UserInfo.objects.filter(username=user_name).first()
        print(f'登录页面获取的user_obj：{user_obj}')
        msg = ''
        if user_obj:
            # 过滤用户
            # print(f'user信息：{user_obj}')
            print(f'登录页面获取的user密码：{user_obj.password}')

            # 密码解密后与数据库对比是否相等,如果返回是True则相等
            if check_password(user_pwd, user_obj.password):
                # 将 session 写到服务器
                request.session['is_login'] = True
                request.session['username'] = user_name
                print('---' * 10)
                print(f'-----：{user_name}')
                print(f'{user_obj.username}的session_id是：{user_obj.id}')

                # 登录成功跳转至文章列表页
                return redirect('article:article_list')
            else:
                msg = '用户名或密码有误！'

        return render(request, 'userprofile/login.html', {'error_msg': msg})

    return render(request, 'userprofile/login.html')


def user_logout(request):
    """用户退出"""
    # logout(request)
    request.session.flush()
    return redirect('article:article_list')


def user_center(request, uid):
    """个人中心"""
    login_status = request.session.get('is_login')
    login_user = request.session.get('username')
    logger.info(f'user_center页面当前登录的用户状态: {login_status},用户名：{login_user}')
    if not login_status:
        return redirect('userprofile:user_login')
    print('------' * 10)

    # 访问我个人中心的用户
    visitor = UserInfo.objects.get(pk=uid)
    logger.info(f'{visitor} 正在访问 {login_user}个人中心页面, user类型：{type(visitor)}')

    # 当前登录的用户
    login_user_id = UserInfo.objects.get(username=login_user).id
    logger.info(f'个人中心当前登录的用户ID：{login_user_id}')

    # user_profile = UserProfile.objects.filter(user__username=user.username).first()
    # user_profile_2 = UserInfo.objects.filter(pk=id).values().filter()
    # logger.info(f'user_profile >>>>: {user_profile}')
    # print(f'user_profile_2 >>>>: {user_profile_2.all()}')

    # 获取我关注的用户信息
    follow_users = FollowUser.objects.filter(source_id=visitor.id).all()
    logger.info(f'follow_users: {follow_users}')

    # 关注的用户列表翻页
    paginator = Paginator(follow_users, 5)
    page = request.GET.get('page')
    logger.info(f'page的内容是: {page}')
    follow_users = paginator.get_page(page)
    logger.info(f'分页拿到的follow_users：{follow_users}')

    # 获取我写的文章
    articles = ArticlePost.objects.filter(author_id=visitor.id).values()

    # 文章列表翻页
    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    logger.info(f'page的内容是: {page}')
    articles = paginator.get_page(page)
    logger.info(f'分页拿到的users：{articles}')

    context = {'login_user_id': login_user_id, "visitor": visitor, 'articles': articles, 'follow_users': follow_users}
    return render(request, 'userprofile/center.html', context)


def modify_icon(request):
    """修改头像"""
    user_name = request.session.get('username')
    # print(f'修改头像页面获取的用户信息：{user_name}')

    # 根据UserProfile表的user跨表查询UserProfile的username
    user = UserProfile.objects.filter(user__username=user_name).first()
    print(f'修改头像获取的user：{user}')
    print(f'user 类型：{type(user)}')

    icon = request.FILES.get('icon')
    print(f'修改头像获取的icon: {icon}')
    print(f'icon类型：{type(icon)}')

    user = UserProfile.objects.get(pk=user.id)
    user.icon = icon
    user.save()

    return JsonResponse({'msg': 'success', 'image': str(user.icon)})


def user_center_edit(request):
    """编辑个人中心"""
    login_status = request.session.get('is_login')
    login_user = request.session.get('username')
    logger.info(f'user_center_edit页面当前登录的用户状态: {login_status},用户名：{login_user}')
    if not login_status:
        return redirect('userprofile:user_login')

    # 过滤用户
    login_user_name = UserInfo.objects.filter(username=login_user).first()

    # 获取用户个人信息
    user_profile = UserProfile.objects.filter(user__username=login_user_name).first()
    print(f'个人中心编辑页面的user_profile: {user_profile}')

    # 获取当前登录用户的id
    login_user_id = UserInfo.objects.get(username=login_user_name).id
    logger.info(f'user_center_edit页面拿到当前登录的用户ID: {login_user_id}')
    # 获取当前登录用户的文章
    article_list = ArticlePost.objects.filter(author_id=login_user_id).values()

    # 获取当前个人中心页面
    profile = UserProfile.objects.filter(user=login_user_id).first()
    if request.method == 'POST':
        # 将提交的表单赋值到表单实例中
        user_profile_form = UserProfileForm(data=request.POST)

        # 判断用户提交的数据是否满足模型的要求
        if user_profile_form.is_valid():
            profile.phone = (request.POST.get('phone'))
            profile.bio = (request.POST.get('bio'))
            profile.micro_blog = (request.POST.get('microblog'))
            profile.save()

            # 重定向到url中带位置参数的两种定义方式
            return redirect('userprofile:user_center', uid=login_user_id)
            # return redirect(f'/userprofile/user_center/{userId}/')

    # 如果用户get请求获取数据，
    else:
        # 创建表单实例
        user_profile_form = UserProfileForm()
        # 赋值上下文，将article文章对象也传递进去，以便提取旧的内容
        context = {'login_user_id': login_user_id, "profile": user_profile, 'articles': article_list, 'user_profile_form': user_profile_form}
        # 将响应返回到模板中
        return render(request, 'userprofile/center_edit.html', context)

    return render(request, 'userprofile/center_edit.html')


'''
# ajax语法搜索
def search(request):
    """用户搜索
    1.判断搜索框输入的数据有效性，
    2.根据搜索框中输入的字符与数据库进行模糊查询
    3.根据数据库里查询出来的用户数据进行精确查询
    """
    # 获取搜索框输入的内容
    search_word = request.POST.get('search_word')
    logger.info(f'搜索框输入的内容是: {search_word}，数据类型是：{type(search_word)}')

    if len(search_word) == 0:
        resp = {"msg": "success", "result": '暂无相关信息'}
        logger.info(f'data数据类型是：{type(resp)}')
        return JsonResponse(resp)
    else:
        if search_word.isdigit():
            user = UserProfile.objects.filter(user=int(search_word)).first()
            logger.info(f'匹配数据库中的user信息是：{user.icon}')

        else:
            user = UserInfo.objects.filter(Q(username__icontains=search_word)).first()
            logger.info(f'匹配数据库中的user信息是：{user.username}')

            resp = {"msg": "success", "result": str(user.username)}
            logger.info(f'data数据类型是：{type(resp)}')

            return JsonResponse(resp)

    return render(request, 'userprofile/center.html')
'''


def ajax_demo1(request):
    return render(request, "userprofile/ajax_demo1.html")


def ajax_add(request):
    """ajax调试"""
    i1 = int(request.GET.get("i1"))
    i2 = int(request.GET.get("i2"))
    ret = i1 + i2
    return JsonResponse(ret, safe=False)
    # return render(request,'index.html')  #返回一个页面没有意义，就是一堆的字符串，拿到了这个页面，你怎么处理，你要做什么事情，根本就没有意义


def user_list(request):
    """所有用户"""
    login_status = request.session.get('is_login')
    user_name = request.session.get('username')
    logger.info(f'user_list页面拿到的登录用户状态：{login_status}，用户名: {user_name}')

    if not login_status:
        return redirect('userprofile:user_login')
    # 获取当前登录的用户id
    login_user_id = UserInfo.objects.get(username=user_name).id
    logger.info(f'user_list页面视图拿到的登录用户ID是: {login_user_id}')

    # 获取UserInfo表里的用户名
    # 其中user_center是UserProfile模型关联UserInfo模型中定义的related_name，作用是跨表查询
    users = UserInfo.objects.all().order_by('pk').values('id', 'username', 'user_center__icon', 'age')
    logger.info(f'用户总数：{users.count()}')
    logger.info(f'用户明细：{users}')

    search = request.GET.get('search')
    logger.info(f'搜索输入框里的内容：{search}')

    # 文章搜索
    if search:
         users = UserInfo.objects.filter(Q(username__icontains=search) | Q(id__icontains=search))
    else:
        # 将search参数重置为空
        search = ''
        """
        # 为什么需要search = ''语句？如果用户没有搜索操作，则search = request.GET.get('search')会使得search = None，
        # 而这个值传递到模板中会错误地转换成"None"字符串！等同于用户在搜索“None”关键字，这明显是错误的
        """
        users = UserInfo.objects.all().order_by('pk').values('id', 'username', 'user_center__icon', 'age')

    # 定义每页显示多少篇
    paginator = Paginator(users, 10)
    # 获取url中的页码
    page = request.GET.get('page')
    logger.info(f'page的内容是: {page}')

    # 将导航对象相应的页码内容返回给users
    users = paginator.get_page(page)
    logger.info(f'分页拿到的users：{users}')

    return render(request, 'userprofile/user_list.html', {'userId': login_user_id, 'users': users}, locals())


def follow_user(request, follow_user_id):
    """关注用户"""
    login_status = request.session.get('is_login')
    user = request.session.get('username')
    print('----' * 10)
    print(type(user))
    logger.info(f'当前登录用户：{user}，登录状态: {login_status}')
    # 获取当前登录的用户id
    login_user_id = UserInfo.objects.get(username=user).id
    logger.info(f'follow_user页面视图拿到的登录用户ID是: {login_user_id}')

    follow_object = FollowUser.objects.filter(source_id=login_user_id, user_id=follow_user_id).all()
    logger.info(f'查询我关注的用户记录: {follow_object}')

    # 获取ajax请求入参并序列化成python对象
    follow = json.loads(request.POST.get('follow'))

    resp = {}   # 定义响应参数
    # FollowUser表里没有关注记录
    if not follow_object:
        # 初次关注按钮
        if follow == True:
            FollowUser.objects.create(source_id=login_user_id, user_id=follow_user_id)
            resp['follow_object'] = False
            resp['follow'] = True
            resp['msg'] = '关注成功！'

        # FollowUser表中无记录，初次点击取消关注按钮
        else:
            resp['follow_object'] = False
            resp['follow'] = False
            resp['msg'] = '您还未关注该用户！'

    # FollowUser表里有关注记录
    else:
        # 再次点击关注按钮
        if follow == True:
            resp['follow_object'] = True
            resp['follow'] = True
            resp['msg'] = '您已关注过该用户！'

        # 取消关注则删除FollowUser表中的记录
        else:
            FollowUser.objects.filter(source_id=login_user_id, user_id=follow_user_id).delete()
            resp['follow_object'] = True
            resp['follow'] = False
            resp['msg'] = '取消关注成功！'

    return JsonResponse(resp)


def read_parent_index(request, author_id):
    """访问关注你的人的个人中心页面"""
    login_status = request.session.get('is_login')
    login_user = request.session.get('username')
    print('----' * 10)
    print(type(login_user))
    logger.info(f'当前登录用户：{login_user}，登录状态: {login_status}')

    # 获取当前登录的用户id
    login_user_id = UserInfo.objects.get(username=login_user).id
    logger.info(f'read_parent_index视图拿到的登录用户ID是: {login_user_id}')

    # 获取FollowUser表中有关注过你的对象
    follow_object = FollowUser.objects.filter(source_id=author_id, user_id=login_user_id).all()
    logger.info(f'查询我关注的用户记录: {follow_object}')

    resp = {}
    # FollowUser表中无关注记录
    if not follow_object:
        # 初次关注按钮
        resp['follow_object'] = False
        resp['msg'] = '暂无权限查看作者的主页'

    # 有权限则跳转至
    else:
        resp['follow_object'] = True
        resp['msg'] = '有权限查看作者的主页'
        # return render(request, 'userprofile/center.html')

    return JsonResponse(resp)

