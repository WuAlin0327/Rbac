
from django.contrib import admin
from django.urls import path,include
from rbac.views import role
from rbac.views import user
from rbac.views import menu
app_name='rbac'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('role/list/',role.role_list,name='role_list'),
    path('role/add/',role.role_add,name='role_add'),
    path('role/edit/<int:num>/',role.role_edit,name='role_edit'),
    path('role/del/<int:num>/',role.role_del,name='role_del'),


    path('user/list/',user.user_list,name='user_list'),
    path('user/add/',user.user_add,name='user_add'),
    path('user/edit/<int:num>/',user.user_edit,name='user_edit'),
    path('user/del/<int:num>/',user.user_del,name='user_del'),
    path('user/reset_password/<int:num>/',user.reset_password,name='user_reset'),

    path('menu/list/',menu.menu_list,name='menu_list'),
    path('menu/menu_add/',menu.menu_add,name='menu_add'),
    path('menu/del/<int:num>/',menu.menu_del,name='menu_del'),
    path('menu/edit/<int:num>/',menu.menu_edit,name='menu_edit'),

]