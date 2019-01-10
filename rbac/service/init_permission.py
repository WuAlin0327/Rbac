from django.conf import settings


def init_permission(request, current_user):
    """
    用户权限初始化
    :param request:请求相关数据
    :param current_user: 从数据库取出的用户对象
    :return:
    """
    # 获取当用户所拥有的所有角色并且根据跨表查询字段查询出角色所拥有的url权限
    permission_queryset = current_user.roles.filter(permission__isnull=False).values('permission__url',
                                                                                     'permission__menu_id',
                                                                                     'permission__menu__title',
                                                                                     'permission__menu__icon',
                                                                                     'permission__title',
                                                                                     'permission__pid__id',
                                                                                     'permission__pid__title',
                                                                                     'permission__pid__url',
                                                                                     'permission__id',
                                                                                     'permission__name'
                                                                                     ).distinct()
    permission_dict = {}
    menu_dict = {}
    for item in permission_queryset:
        permission_dict[item['permission__name']]={
                'id': item['permission__id'],
                'url': item['permission__url'],
                'title':item['permission__title'],
                'pid': item['permission__pid__id'],
                'p_title':item['permission__pid__title'],
                'p_url':item['permission__pid__url'],
            }

        menu_id = item['permission__menu_id']

        if not menu_id:
            continue
        # 组成二级菜单需要的数据结构
        node = {'id': item['permission__id'], 'title': item['permission__title'], 'url': item['permission__url']}
        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append(node)
        else:
            menu_dict[menu_id] = {
                'title': item['permission__menu__title'],
                'icon': item['permission__menu__icon'],
                'children': [node, ]
            }
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.PERMISSION_SESSION_MENU] = menu_dict
