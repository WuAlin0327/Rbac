from django.db import models

# Create your models here.

class Permission(models.Model):
    '''
    权限表
    '''
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标题',max_length=32)
    url = models.CharField(verbose_name='含正则的URL',max_length=128)
    name = models.CharField(verbose_name='URL的别名', max_length=32, unique=True)
    menu = models.ForeignKey(verbose_name='所属菜单',to='Menu',to_field='id',null=True,help_text='null表示不是菜单,非null表示是二级菜单',blank=True,on_delete=True)
    # icon = models.CharField(verbose_name='图标',max_length=32,null=True,blank=True)
    pid = models.ForeignKey(verbose_name='关联的权限',to='Permission',null=True,blank=True,related_name='parent',on_delete=True,help_text='对于非菜单权限需要选择一个可以成为菜单的权限，用户做默认展开和选中菜单')



    def __str__(self):
        return self.title
class Role(models.Model):
    """
    角色表
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='角色昵称',max_length=32)
    permission = models.ManyToManyField(verbose_name='所拥有的权限',to=Permission,blank=True)

    def __str__(self):
        return self.title
class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名',max_length=32)
    email = models.EmailField(verbose_name='邮箱',null=True)
    password = models.CharField(verbose_name='密码',max_length=16)
    roles = models.ManyToManyField(verbose_name='用户的角色',to=Role)
    create_data = models.DateField(auto_created=True,null=True)

    def __str__(self):
        return self.username


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='一级菜单名称',max_length=32)
    icon = models.CharField(verbose_name='图标',max_length=32)

    def __str__(self):
        return self.title



