from rbac import models
from django import forms
from django.core.exceptions import ValidationError

class UserModelForm(forms.ModelForm):
    r_password = forms.CharField(label='确认密码',widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = models.UserInfo
        fields = ['username','email','password','r_password']
        # widgets = {
        #     'username':forms.TextInput(attrs={'class':'form-control'}),
        #     'email':forms.EmailInput(attrs={'class':'form-control'}),
        #     'password': forms.TextInput(attrs={'class': 'form-control',}),
        # }

    def __init__(self,*args,**kwargs):
        """
        统一给ModelForm字段构建样式
        :param args:
        :param kwargs:
        """
        super(UserModelForm, self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


    def clean_r_password(self):
        """
        钩子函数
        :return:
        """
        password = self.cleaned_data['password']
        r_password = self.cleaned_data['r_password']
        if password != r_password:
            raise ValidationError('两次密码输入不一致')

        return r_password

class UpdateUserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['username','email']
        # widgets = {
        #     'username':forms.TextInput(attrs={'class':'form-control'}),
        #     'email':forms.EmailInput(attrs={'class':'form-control'}),
        #     'password': forms.TextInput(attrs={'class': 'form-control',}),
        # }

    def __init__(self,*args,**kwargs):
        """
        统一给ModelForm字段构建样式
        :param args:
        :param kwargs:
        """
        super(UpdateUserModelForm, self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ResetPasswordModelForm(forms.ModelForm):
    """
    重置密码
    """
    r_password = forms.CharField(label='确认密码',widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = models.UserInfo
        fields = ['password']

    def __init__(self,*args,**kwargs):
        """
        统一给ModelForm字段构建样式
        :param args:
        :param kwargs:
        """
        super(ResetPasswordModelForm, self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_r_password(self):
        """
        钩子函数
        :return:
        """
        password = self.cleaned_data['password']
        r_password = self.cleaned_data['r_password']
        if password != r_password:
            raise ValidationError('两次密码输入不一致')

        return r_password

