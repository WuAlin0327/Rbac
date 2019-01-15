from django.shortcuts import HttpResponse,render,redirect
from rbac.models import UserInfo # 根据实际情况进行更改
from rbac.service.init_permission import init_permission
def login(request):
    if request.method =='GET':
        return render(request,'login.html')

    # 1.  用户登陆
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    current_user = UserInfo.objects.filter(username=user, password=pwd).first()
    if not current_user:
        msg = '登陆失败，用户或者密码错误'
        return render(request, 'login.html', {'msg': msg})
    

    # 根据当前用户信息获取此用户所拥有的所有权限，并放入session
    # 2. 权限信息初始化（重要）
    init_permission(request,current_user)
    return redirect('/customer/list/')

def logout(request):
    request.session.delete()
    return redirect('/login/')


