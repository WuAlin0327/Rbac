"""
角色管理
"""
from django.shortcuts import render,redirect,HttpResponse
from rbac import models
from rbac.forms.role import RoleModelForm
from django.urls import reverse




def role_list(request):
    """
    角色列表
    :param request:
    :return:
    """
    role_queryset = models.Role.objects.all()
    return render(request, 'rbac/role_list.html', {'roles':role_queryset})


def role_add(request):
    """
    添加角色
    :param request:
    :return:
    """

    if request.method =='POST':
        form = RoleModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('rbac:role_list'))
        else:
            return render(request, 'rbac/change.html', {'form': form})
    form = RoleModelForm()
    return render(request, 'rbac/change.html', {'form':form})

def role_edit(request,num):
    """
    更改角色
    :param request:
    :param num:
    :return:
    """
    obj = models.Role.objects.filter(pk=num)
    if not obj.first():
        response = HttpResponse('角色不存在')
        response.status_code = 404
        return response
    if request.method =='GET':
        form = RoleModelForm(instance=obj.first())
        return render(request, 'rbac/change.html', {'form':form})

    form = RoleModelForm(instance=obj.first(),data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))
    return render(request, 'rbac/change.html', {'form': form})


def role_del(request,num):
    """
    删除角色
    :param request:
    :param num:
    :return:
    """
    origin_url = reverse('rbac:role_list')
    if request.method == 'GET':
        role = models.Role.objects.filter(id=num).first()
        return render(request,'rbac/delete.html',{'role':role,'cancel':origin_url})
    models.Role.objects.filter(id=num).delete()
    return redirect(origin_url)