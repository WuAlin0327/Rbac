## Rbac(基于角色的权限管理组件)使用文档
1. 复制rbac到你的项目中
2. 将rbac/migtations中的迁移记录删除


### 业务系统
1. 业务系统中用户表结构设计：业务表结构中的用户表需要和rbac中的用户有继承关系

业务/models.py
```
from rbac.models import UserInfo as RbacUserInfo
class UserInfo(RbacUserInfo):
    phone = models.CharField(verbose_name='联系方式',max_length=32)
    level_choices = (
        (1,'T1'),
        (2,'T2'),
        (3,'T3')
    )
    level = models.IntegerField('级别',choices=level_choices)
```
rbac/models.py
```
...
class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名',max_length=32)
    email = models.EmailField(verbose_name='邮箱',null=True)
    password = models.CharField(verbose_name='密码',max_length=16)
    roles = models.ManyToManyField(verbose_name='用户的角色',to=Role)# Role不要加引号，否则会报错
    create_data = models.DateField(auto_created=True,null=True)

    def __str__(self):
        return self.username
```
2. 将业务系统中的用户表的路径写到配置文件中。用于在rbac分配权限时，读取业务表中的用户信息
```
RBAC_USER_MODEL_CLASS = 'app01.models.UserInfo'
```
3. 业务逻辑开发
将所有的路由都设置name属性，name不能重复,用于反向生成URL以及粒度控制到按钮级别的权限控制

如：
```
urlpatterns = [

    url(r'^customer/list/$', customer.customer_list,name='customer_list'),
    url(r'^customer/add/$', customer.customer_add,name='customer_add'),
    url(r'^customer/edit/(?P<cid>\d+)/$', customer.customer_edit,name='customer_edit'),
    url(r'^customer/del/(?P<cid>\d+)/$', customer.customer_del,name='customer_del'),
    url(r'^customer/import/$', customer.customer_import,name='customer_import'),
    url(r'^customer/tpl/$', customer.customer_tpl,name='customer_tpl'),

    url(r'^payment/list/$', payment.payment_list,name='payment_list'),
    url(r'^payment/add/$', payment.payment_add,name='payment_add'),
    url(r'^payment/edit/(?P<pid>\d+)/$', payment.payment_edit,name='payment_edit'),
    url(r'^payment/del/(?P<pid>\d+)/$', payment.payment_del,name='payment_del'),
    url(r'^login/$',account.login,name='login'),
    url('^logout/$',account.logout,name='logout')
]
```

### 权限信息录入
相关配置：自动发现权限时过滤的权限
```
AUTO_EXCLUDE_LIST = [
        '/admin/.*',
        '/login/',
        '/logout/',
        '/index/'
    ]
```
在根路由添加rbac的路由分发，必须设置namespace='rbac'
```
urlpatterns = [
    ...
    url(r'^rbac/',include('rbac.urls',namespace='rbac')),
]
```
rbac提供的地址进行操作
```
http://127.0.0.1:8000/rbac/menu/list/ # 菜单列表

http://127.0.0.1:8000/rbac/multi/permission/ # 批量操作(增加，删除，更新)权限

http://127.0.0.1:8000/rbac/role/list/ # 角色列表

http://127.0.0.1:8000/rbac/distribute/permission # 用户分配角色，角色分配权限
```
### 用户登陆权限处理【进行权限初始化】
相关的配置:权限和菜单的session_key
```
PERMISSION_SESSION_KEY = 'permission_list'
PERMISSION_SESSION_MENU = 'permission_menu_list'
```
设置需要登陆但是不需要进行权限校验的url
```
NO_PERMISSION_URL = [
    '/logout/',
    '/index/'
]
```
```
from django.shortcuts import HttpResponse,render,redirect
from rbac.models import UserInfo # 根据实际情况进行更改
from rbac.service.init_permission import init_permission # 重要
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
```

### 通过中间件进行权限校验
```
# 配置中间件
MIDDLEWARE = [
                ...
                ...
    'rbac.middleware.rbac.RbacMiddleware'

]

# 白名单：所有人都可以访问的url
VALID_URL_LIST = [
        '/login/',
        '/admin/.*',
]
```
### 粒度控制到按钮级别
控制一个用户是否拥有该a标签或者按钮的权限去显示或者隐藏该按钮，必须某个用户只有查看用户列表的权限，编辑用户与删除用户的按钮不应该显示在页面，rbac组件给该功能提供了一个模板语法。例：判断显示还是隐藏添加客户的按钮
```
# 导入自定义模板
{% load rbac %}
# 固定格式 request|has_permission:url的别名,该模板语法返回值是True或者False，返回True则渲染该按钮
{% if request|has_permission:'customer_add' %}
    <a href='{% url 'customer_add' %}>添加客户</a>
{% endif %}

```

### 总结：目的是希望在任意系统中应用权限系统
- 用户登陆 + 用户首页 + 用户注销 业务逻辑
- 项目业务逻辑开发
    - 开发时灵活的去设置layut.html中的两个inclusion_tag，开发时去掉，上线时放在你layout项目中预留的位置
```
# 渲染菜单
{% multi_menu request %}

# 渲染导航
{% url_record request %}
```
- 权限信息的录入
- 配置文件
```
INSTALLED_APPS = [
            ...
    'rbac.apps.RbacConfig',
]

MIDDLEWARE = [
            ...
    'rbac.middleware.rbac.RbacMiddleware'

]
# 权限相关的配置
PERMISSION_SESSION_KEY = 'permission_list'
PERMISSION_SESSION_MENU = 'permission_menu_list'

# 白名单
VALID_URL_LIST = [
        '/login/',
        '/admin/.*',
]

# 自动发现路由时过滤的url
AUTO_EXCLUDE_LIST = [
        '/admin/.*',
        '/login/',
        '/logout/'
    ]

# 只需要登陆不需要进行权限校验
NO_PERMISSION_URL = [
    '/logout/',
    '/index/'
]

# 业务中UserInfo表的路径
RBAC_USER_MODEL_CLASS = 'app01.models.UserInfo'
```