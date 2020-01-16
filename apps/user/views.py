from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
import re
from user.models import User
# Create your views here.


# /user/register
def register(request):
    '''注册'''
    return render(request,'register.html')

def register_handle(request):
    '''进行注册的处理'''
    #接收数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')
    #数据校验
    if not all([username,password,email]):
        #数据不完整
        return render(request,'register.html',{'errmsg':'数据不完整'})

    if not  re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        return render(request, 'register.html', {'errmsg': '邮箱不合法'})

    if allow != 'on':
        return render(request, 'register.html', {'errmsg': '未勾选协议'})

    #用户名是否重复
    try:
        user= User.objects.get(username=username)
    except User.DoesNotExist:
        #用户名不存在
        user = None

    if user:
        #存在
        return render(request,'register.html',{'errmsg':'用户名已存在'})

    # 处理
    # user = User()
    # user.username=username
    # user.password=password
    # user.save()

    #内置方法 进行用户注册
    user = User.objects.create_user(username,email,password)
    user.is_active=0
    #为0 则不激活
    user.save()
    #应答 跳转到首页  反响解析
    return redirect(reverse('goods:index'))



















