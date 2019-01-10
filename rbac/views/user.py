
from django.shortcuts import redirect,HttpResponse,render
from django.urls import reverse
from rbac.models import UserInfo
from rbac.forms.user import UserModelForm,UpdateUserModelForm,ResetPasswordModelForm

def user_list(request):
    """
    用户列表
    :param request:
    :return:
    """
    users = UserInfo.objects.all()

    return render(request,'rbac/user_List.html',{'users':users})



def user_add(request):
    """
    新增用户
    :param request:
    :return:
    """
    if request.method =='GET':
        form = UserModelForm()
        return render(request,'rbac/change.html',{'form':form})
    form = UserModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request,'rbac/change.html',{'form':form})

def user_edit(request,num):
    """
    编辑用户
    :param request:
    :param num:
    :return:
    """
    obj = UserInfo.objects.filter(id=num)
    if not obj.first():
        return HttpResponse('用户不存在')

    if request.method =='GET':
        form = UpdateUserModelForm(instance=obj.first())
        return render(request,'rbac/change.html',{'form':form})

    form = UpdateUserModelForm(instance=obj.first(),data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request,'rbac/change.html',{'form':form})


def user_del(request,num):
    """
    删除用户
    :param request:
    :param num:
    :return:
    """
    cancel = reverse('rbac:user_list')
    if request.method == 'GET':
        return render(request,'rbac/delete.html',{'cancel':cancel})

    UserInfo.objects.filter(id=num).delete()
    return redirect(cancel)

def reset_password(request,num):
    """
    重置密码
    :param request:
    :param num:
    :return:
    """
    obj = UserInfo.objects.filter(id=num)
    if request.method =='POST':
        form = ResetPasswordModelForm(instance=obj.first(),data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:user_list'))
        else:
            return render(request, 'rbac/change.html', {'form': form})
    form = ResetPasswordModelForm()
    return render(request,'rbac/change.html',{'form':form})


