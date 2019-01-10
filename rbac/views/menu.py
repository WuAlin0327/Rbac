from django.shortcuts import render,redirect,HttpResponse
from rbac.forms.menu import MenuModelForm
from rbac import models
from rbac.service.urls import memory_reverse



def menu_list(request):
    """
    菜单和权限列表
    :param request:
    :return:
    """
    menu = models.Menu.objects.all()
    if not request.GET:
        return render(request,'rbac/menu_list.html',{'menus':menu})
    mid = request.GET.get('mid')
    if mid:
        second_menu = models.Permission.objects.filter(menu_id=mid)

        return render(request, 'rbac/menu_list.html', {'menus': menu,'menu_id':int(mid),'second_menu':second_menu})
    return render(request, 'rbac/menu_list.html', {'menus': menu})

def menu_add(request):
    """
    添加一级菜单
    :param request:
    :return:
    """
    if request.method =='POST':
        form = MenuModelForm(request.POST)
        if form.is_valid():
            form.save()
            url = memory_reverse(request,'rbac:menu_list')
            return redirect(url)
        else:
            return render(request, 'rbac/change.html', {'form': form})
    form = MenuModelForm()
    return render(request, 'rbac/change.html', {'form':form})

def menu_del(request,num):
    url = memory_reverse(request,'rbac:menu_list')

    if request.method == 'GET':
        role = models.Menu.objects.filter(id=num).first()
        return render(request,'rbac/delete.html',{'role':role,'cancel':url})
    models.Menu.objects.filter(id=num).delete()
    return redirect(url)


def menu_edit(request,num):
    """
    一级菜单删除
    :param request:
    :param num:
    :return:
    """
    obj = models.Menu.objects.filter(pk=num)
    url = memory_reverse(request, 'rbac:menu_list')
    if not obj.first():
        response = HttpResponse('角色不存在')
        response.status_code = 404
        return response
    if request.method =='GET':
        form = MenuModelForm(instance=obj.first())
        return render(request, 'rbac/change.html', {'form':form})

    form = MenuModelForm(instance=obj.first(),data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})

