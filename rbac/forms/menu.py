from django import forms
from rbac import models
from rbac.service.get_font import get_font
from .base import BaseModelForm


class MenuModelForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.RadioSelect(
                # 获取字体图标
                choices=get_font()
            )
        }


class SecondMenuModelForm(forms.ModelForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'url', 'name', 'menu']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'menu': forms.Select(attrs={'class': 'form-control'}),
        }


class PermissionModelForm(BaseModelForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'name', 'url']


class MultiAddPermissionForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    menu_id = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=[(None, '------')],
        required=False
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '------')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    def __init__(self,*args,**kwargs):
        super(MultiAddPermissionForm, self).__init__(*args,**kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id','title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True
        ).values_list('id','title')


class UpdatePermissionForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.TextInput(attrs={'class':'hide'})
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    menu_id = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=[(None, '------')],
        required=False
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '------')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    def __init__(self,*args,**kwargs):
        super(UpdatePermissionForm, self).__init__(*args,**kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.all().values_list('id','title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True
        ).values_list('id','title')
