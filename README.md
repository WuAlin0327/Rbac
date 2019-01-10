大目标：crm系统

    - 权限
    - stark组件
    - crm业务
    
步骤：

1. 创建django项目
2. 创建两个app
    - rbac：权限组件
    - web：销售管理系统
3. app：rbac
    - 将权限相关的表编写到此app的models.py中
4. app：web
    - 将销售系统相关的表编写到此app的models中
5. 两个app的整合
    - 销售管理系统中的url：
客户管理：
```
客户列表：/customer/list/
添加客户：/customer/add/
删除客户：/customer/list/(?P<cid>\d+)/
修改客户：/customer/edit/(?P<cid>\d+)/
批量导入：/customer/import/
下载模版：/customer/tpl/
```
账单管理:
```
账单列表:/payment/list/
添加账单:/payment/add/
删除账单:/payment/del/(?P<pid>\d+)/
修改账单:/payment/edit/(?P<pid>\d+)/
```
5.1 基于admin进行权限信息的录入
5.2 基于admin进行权限和角色信息的分配

6. 快速完成一个基本的权限控制
```
1. 登陆页面是否有权限访问
2. post请求，用户登陆校验是否合法
3. 获取当前用户相关的所有权限并放入session
4. 再次向服务端发起请求，django编写中间件对用户当前访问的url进行权限判断(是否在session中)
```
7. 动态菜单的功能

    - 一级菜单
    - 二级菜单
8. 点击非菜单的权限时，默认选中或默认展开
9. 路径导航
10. 权限粒度控制到按钮级别
    - 判断用户是否有当前权限，如果有就显示，没有就不显示
总结：开发完简单的权限控制
- 权限控制：在中间件中对权限进行判断
- 动态菜单功能
- 权限的分配

11. 权限分配开发功能
    - 角色管理
    - 用户管理
    - 菜单和权限管理
    - 权限的批量操作
    - 权限的分配

