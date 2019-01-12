from django.shortcuts import render, redirect, HttpResponse
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm, PermissionModelForm, UpdatePermissionForm,MultiAddPermissionForm
from rbac import models
from rbac.service.urls import memory_reverse
from django.forms import formset_factory
from rbac.service.get_url import get_all_url_dict
from collections import OrderedDict


def menu_list(request):
    """
    菜单和权限列表
    :param request:
    :return:
    """
    menu = models.Menu.objects.all()
    if not request.GET:
        return render(request, 'rbac/menu_list.html', {'menus': menu})
    mid = request.GET.get('mid')
    if mid:
        second_menu = models.Permission.objects.filter(menu_id=mid)
        second_id = request.GET.get('sid')
        if second_id:
            # 如果前端传过来的sid存在的话
            # http://127.0.0.1:8000/rbac/menu/list/?mid=1&sid=1
            permission_list = models.Permission.objects.filter(pid=second_id)

            # 判断前端传过来的second_id是否存在，如果不存在则不显示新增按钮
            second_list = models.Permission.objects.filter(id=second_id)
            if not second_list:
                second_id = 0
            return render(request, 'rbac/menu_list.html',
                          {
                              'menus': menu,
                              'menu_id': int(mid),
                              'second_menu': second_menu,
                              'sid': int(second_id),
                              'permission_list': permission_list
                          })
        return render(request, 'rbac/menu_list.html',
                      {
                          'menus': menu,
                          'menu_id': int(mid),
                          'second_menu': second_menu,
                      })
    return render(request, 'rbac/menu_list.html', {'menus': menu})


def menu_add(request):
    """
    添加一级菜单
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = MenuModelForm(request.POST)
        if form.is_valid():
            form.save()
            url = memory_reverse(request, 'rbac:menu_list')
            return redirect(url)
        else:
            return render(request, 'rbac/change.html', {'form': form})
    form = MenuModelForm()
    return render(request, 'rbac/change.html', {'form': form})


def menu_del(request, num):
    url = memory_reverse(request, 'rbac:menu_list')

    if request.method == 'GET':
        role = models.Menu.objects.filter(id=num).first()
        return render(request, 'rbac/delete.html', {'role': role, 'cancel': url})
    models.Menu.objects.filter(id=num).delete()
    return redirect(url)


def menu_edit(request, num):
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
    if request.method == 'GET':
        form = MenuModelForm(instance=obj.first())
        return render(request, 'rbac/change.html', {'form': form})

    form = MenuModelForm(instance=obj.first(), data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_add(request, menu_id):
    """
    添加二级菜单
    :param request:
    :param menu_id: 已选择的一级菜单ID（用于设置默认选中）
    :return:
    """
    menu_obj = models.Menu.objects.filter(id=menu_id).first()
    if request.method == 'POST':
        form = SecondMenuModelForm(request.POST)
        if form.is_valid():
            form.save()
            url = memory_reverse(request, 'rbac:menu_list')
            return redirect(url)
        else:
            return render(request, 'rbac/change.html', {'form': form})
    form = SecondMenuModelForm(initial={'menu': menu_obj})
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_del(request, num):
    url = memory_reverse(request, 'rbac:menu_list')

    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Permission.objects.filter(id=num).delete()
    return redirect(url)


def second_menu_edit(request, num):
    obj = models.Permission.objects.filter(pk=num)
    url = memory_reverse(request, 'rbac:menu_list')
    if not obj.first():
        response = HttpResponse('角色不存在')
        response.status_code = 404
        return response
    if request.method == 'GET':
        form = SecondMenuModelForm(instance=obj.first())
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForm(instance=obj.first(), data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})


def permission_add(request, second_id):
    """
    添加权限
    :param request:
    :param second_id:
    :return:
    """
    if request.method == 'POST':
        form = PermissionModelForm(request.POST)
        if form.is_valid():
            second_menu_obj = models.Permission.objects.filter(id=second_id).first()
            if not second_menu_obj:
                return HttpResponse('二级菜单不存在，请重新选择')
            # form.instance中包含用户提交的所有值,相当于写了下面两段代码
            # instance = models.Permission(title='',name='',url='')
            # instance.id = second_menu_obj
            form.instance.pid = second_menu_obj
            form.save()
            url = memory_reverse(request, 'rbac:menu_list')
            return redirect(url)
        else:
            return render(request, 'rbac/change.html', {'form': form})
    form = PermissionModelForm()
    return render(request, 'rbac/change.html', {'form': form})


def permission_del(request, second_id):
    url = memory_reverse(request, 'rbac:menu_list')

    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Permission.objects.filter(id=second_id).delete()
    return redirect(url)


def permission_edit(request, second_id):
    obj = models.Permission.objects.filter(pk=second_id)
    url = memory_reverse(request, 'rbac:menu_list')
    if not obj.first():
        response = HttpResponse('角色不存在')
        response.status_code = 404
        return response
    if request.method == 'GET':
        form = PermissionModelForm(instance=obj.first())
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForm(instance=obj.first(), data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(url)
    return render(request, 'rbac/change.html', {'form': form})

#
# def permission_batch_add(request):
#     # 先实例出formset对象，参数一是需要渲染的ModelForm,第二个参数是需要增加多少个
#     form_class = formset_factory(BatchPermissionModelForm, extra=2)
#
#     if request.method == 'POST':
#         # post请求，提交数据
#         formset = form_class(data=request.POST)  # 把接受到的数据放到formset中
#         if formset.is_valid():  # 使用formset表单进行验证
#             post_data = formset.cleaned_data  # 先取出验证成功后的数据
#             flag = True
#             for i in range(0, formset.total_form_count()):  # 循环
#                 # 检测保存时是否会出现错误，如果出现错误捕获错误放到errors中再在页面中渲染出来
#                 row_data = post_data[i]
#                 if not row_data:
#                     continue
#                 try:
#                     print(row_data)
#                     obj = models.Permission(**row_data)
#                     obj.validate_unique()
#                     # obj.save()
#                 except Exception as e:
#                     formset.errors[i].update(e)
#                     flag = False
#             if flag:
#                 return HttpResponse('增加成功')
#             else:
#                 render(request, 'rbac/multi_permission.html', {'formset': formset})
#         else:
#             render(request, 'rbac/multi_permission.html', {'formset': formset})
#
#     # get请求页面，将需要渲染的form表单传到模板，在模板中渲染
#     formset = form_class()
#     return render(request, 'rbac/multi_permission.html', {'formset': formset})




def multi_permission(request):
    """
    批量操作权限:获取项目中所有的URL
    :param request:
    :return:
    """
    # 1.获取项目中所有的url
    all_url_dict = get_all_url_dict()
    router_name_set = set(all_url_dict.keys())
    """
    {
        'rbac:menu_add':{'name': 'rbac:menu_add', 'url': '/rbac/menu/menu_add/'},
        'rbac:menu_del':{'name': 'rbac:menu_del', 'url': '/rbac/menu/del/<int:num>/'}
        ...
    }
    
    """

    # 2.获取数据库中所有的URL
    permission = models.Permission.objects.all().values('id','title','name','url','menu_id','pid_id')
    permission_ordered_dict =OrderedDict()
    """
        'customer_list':{'id': 1, 'title': '客户列表', 'name': 'customer_list', 'url': '/customer/list/', 'menu_id': 1, 'pid_id': None}
        ...
    """
    for row in permission:
        permission_ordered_dict[row['name']] = row
    permission_name_set = set(permission_ordered_dict.keys())

    # 判断获取的路由URL是否和数据库中URL一致
    for name,value in permission_ordered_dict.items():
        router_row_dict = all_url_dict.get(name)
        if not router_row_dict:
            continue
        if value['url'] != router_row_dict['url']:
            value['url'] = '路由和数据库中不一致'



    # 3.应该添加，删除，修改的权限有哪些
    generate_name_list = router_name_set - permission_name_set # 应该需要增加的
    generate_formset_class = formset_factory(MultiAddPermissionForm,extra=0)
    generate_formset = generate_formset_class(
        initial=[ row_dict for row,row_dict in all_url_dict.items() if row in generate_name_list]
    )


    # 计算出应该删除的name
    delete_name_list = permission_name_set - router_name_set # 应该删除的
    delete_row_list = [row_dict for name,row_dict in permission_ordered_dict.items() if name in delete_name_list]


    # 计算出应该修改的name。必须要有一个隐藏的id
    update_name_list = permission_name_set & router_name_set# 应该更新的
    update_formset_class = formset_factory(UpdatePermissionForm,extra=0)
    update_formset = generate_formset_class(
        initial=[ row_dict for name,row_dict in permission_ordered_dict.items() if name in update_name_list]
    )


    return render(request,'rbac/')
