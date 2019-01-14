
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from rbac.views import role
from rbac.views import user
from rbac.views import menu
app_name='rbac'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('role/list/',role.role_list,name='role_list'),
    path('role/add/',role.role_add,name='role_add'),
    url(r'^role/edit/(?P<num>\d+)/$',role.role_edit,name='role_edit'),
    url(r'^role/del/(?P<num>\d+)/$',role.role_del,name='role_del'),


    path('user/list/',user.user_list,name='user_list'),
    path('user/add/',user.user_add,name='user_add'),
    url(r'^user/edit/(?P<num>\d+)/$',user.user_edit,name='user_edit'),
    url(r'^user/del/(?P<num>\d+)/$',user.user_del,name='user_del'),
    url(r'^user/reset_password/(?P<num>\d+)/$',user.reset_password,name='user_reset'),

    path('menu/list/',menu.menu_list,name='menu_list'),
    path('menu/menu_add/',menu.menu_add,name='menu_add'),
    url(r'^menu/del/(?P<num>\d+)/',menu.menu_del,name='menu_del'),
    url(r'^menu/edit/(?P<num>\d+)/',menu.menu_edit,name='menu_edit'),

    url(r'^second/second_add/(?P<num>\d+)/$', menu.second_menu_add, name='second_menu_add'),
    url(r'^second/del/(?P<num>\d+)/$', menu.second_menu_del, name='second_menu_del'),
    url(r'^second/edit/(?P<num>\d+)/$', menu.second_menu_edit, name='second_menu_edit'),

    url(r'^permission/add/(?P<second_id>\d+)/$', menu.permission_add,name='permission_add'),
    url(r'^permission/del/(?P<second_id>\d+)/$', menu.permission_del,name='permission_del'),
    url(r'^permission/edit/(?P<second_id>\d+)/$', menu.permission_edit,name='permission_edit'),

    # 批量操作

    path('multi/permission/',menu.multi_permission,name='multi_permission'),
    url(r'^multi/permission/del/(?P<id>\d+)/$',menu.multi_permission_del,name='multi_permission_del'),

    # 分配权限
    path('distribute/permission',menu.distribute_permission,name='distribute_permission')


]