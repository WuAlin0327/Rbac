from django import template
from django.conf import settings

import re
from collections import OrderedDict
from rbac.service.urls import memory


register = template.Library()


@register.inclusion_tag('rbac/static_menu.html')
def static_menu(request):
    """
    创建一级菜单

    找到装饰器参数中的模板文件，
    :return:
    """
    menu_list = request.session[settings.PERMISSION_SESSION_MENU]
    return {'menu_list':menu_list,'path_info':request.path_info}

@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    """
     二级菜单
    :param request:
    :return:
    """
    menu_dict = request.session[settings.PERMISSION_SESSION_MENU]
    key_list = sorted(menu_dict)

    # 创建一个空的有序字典
    ordered_dict = OrderedDict()
    for key in key_list:
        val = menu_dict[key]
        val['class'] = 'second_menu_body'
        for per in val['children']:
            # 判断选中url是否与当前的链接一样，如果一样的话给选中的标签添加一个active样式
            if per['id'] == request.selected_id:
                per['class'] = 'active'
                val['class'] = ''
        ordered_dict[key] = val
    menu_dict = ordered_dict

    return {'menu_dict': menu_dict, 'path_info': request.path_info}

@register.inclusion_tag('rbac/record.html')
def url_record(request):
    """
    路径导航
    :param request:
    :return:
    """

    record = request.url_record

    return {
        'record':record
    }

@register.filter
def has_permission(request,name):
    """
    判断是否有权限

    @register.filter最多只有两个参数
    第一个参数|函数名:第二个参数
    :param request:
    :param name:
    :return:
    """
    if name in request.session[settings.PERMISSION_SESSION_KEY]:
        return True
    return False

@register.simple_tag()
def memory_url(request,name,*args,**kwargs):
    """
    生成带有原搜索条件的URL
    记忆上次访问状态
    :return:
    """
    url = memory(request,name,*args,**kwargs)

    return url


