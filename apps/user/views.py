from django.shortcuts import render

# Create your views here.


# /user/register
def register(request):
    '''注册'''
    return render(request,'register.html')

def register_handle(request):
    '''进行注册的处理'''
    pass




















