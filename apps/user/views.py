from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
import re
from django.views.generic import View
from user.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from itsdangerous import SignatureExpired
from django.http import HttpResponse
from django.core.mail import send_mail
# Create your views here.


# # /user/register
# def register(request):
#     '''注册'''
#     if request.method=='GET':
#         return render(request,'register.html')
#     else:
#         # 接收数据
#         username = request.POST.get('user_name')
#         password = request.POST.get('pwd')
#         email = request.POST.get('email')
#         allow = request.POST.get('allow')
#         # 数据校验
#         if not all([username, password, email]):
#             # 数据不完整
#             return render(request, 'register.html', {'errmsg': '数据不完整'})
#
#         if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
#             return render(request, 'register.html', {'errmsg': '邮箱不合法'})
#
#         if allow != 'on':
#             return render(request, 'register.html', {'errmsg': '未勾选协议'})
#
#         # 用户名是否重复
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             # 用户名不存在
#             user = None
#
#         if user:
#             # 存在
#             return render(request, 'register.html', {'errmsg': '用户名已存在'})
#
#         # 处理
#         # user = User()
#         # user.username=username
#         # user.password=password
#         # user.save()
#
#         # 内置方法 进行用户注册
#         user = User.objects.create_user(username, email, password)
#         user.is_active = 0
#         # 为0 则不激活
#         user.save()
#         # 应答 跳转到首页  反响解析
#         return redirect(reverse('goods:index'))

# def register_handle(request):
#     '''进行注册的处理'''
#     #接收数据
#     username = request.POST.get('user_name')
#     password = request.POST.get('pwd')
#     email = request.POST.get('email')
#     allow = request.POST.get('allow')
#     #数据校验
#     if not all([username,password,email]):
#         #数据不完整
#         return render(request,'register.html',{'errmsg':'数据不完整'})
#
#     if not  re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
#         return render(request, 'register.html', {'errmsg': '邮箱不合法'})
#
#     if allow != 'on':
#         return render(request, 'register.html', {'errmsg': '未勾选协议'})
#
#     #用户名是否重复
#     try:
#         user= User.objects.get(username=username)
#     except User.DoesNotExist:
#         #用户名不存在
#         user = None
#
#     if user:
#         #存在
#         return render(request,'register.html',{'errmsg':'用户名已存在'})
#
#     # 处理
#     # user = User()
#     # user.username=username
#     # user.password=password
#     # user.save()
#
#     #内置方法 进行用户注册
#     user = User.objects.create_user(username,email,password)
#     user.is_active=0
#     #为0 则不激活
#     user.save()
#     #应答 跳转到首页  反响解析
#     # return redirect(reverse('goods:index'))

class RegisterView(View):
    '''注册'''
    def get(self,request):
        '''显示注册'''
        return render(request,'register.html')

    def post(self,request):
        '''注册处理'''
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱不合法'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '未勾选协议'})

        # 用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            # 存在
            return render(request, 'register.html', {'errmsg': '用户名已存在'})
        # 处理
        # user = User()
        # user.username=username
        # user.password=password
        # user.save()

        # 内置方法 进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        # 为0 则不激活
        user.save()

        #发送激活邮件  http://127.0.0.1:8000/user/active/3
        #拿到jdango中设置中的settings.SECRET_KEY  然后拿到用户id 组合加密
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info)

        #发送邮件
        #标题
        subject = '生鲜信息欢迎你'
        message = '<h1>%s,欢迎您成为会员，</h1点击下链接激活用户</br><a href="http:127.0.0.1:8000/user/active/%s">http:127.0.0.1:8000/user/active/%s</a>'%(username,token,token)
        sender = settings.EMAIL_FROM
        receiver = [email]
        send_mail(subject,message,sender,receiver)

        # 应答 跳转到首页  反响解析
        return redirect(reverse('goods:index'))

class ActiveView(View):
    '''用户激活'''
    def get(self,request,token):
        '''进行用户激活'''
        #解密  获取用户所需要的信息
        serializer = Serializer(settings.SECRET_KEY,3600)
        try:
            info = serializer.loads(token)
            #获取待激活用户的ID
            user_id = info['confirm']
            #根据用户拿到id
            user = User.objects.get(id=user_id)
            user.is_active=1
            user.save()
            #跳转到login页面
            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            #激活链接已经过期
            return HttpResponse("激活链接已经过期")

# /user/login
class LoginView(View):
    '''登陆首页'''
    def get(self,request):
        '''显示登陆页面'''
        return render(request,'login.html')





