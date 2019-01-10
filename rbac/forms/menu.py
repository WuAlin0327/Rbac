from django import forms
from rbac import models
from rbac.service.get_font import get_font

class MenuModelForm(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = '__all__'
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'icon':forms.RadioSelect(
                # 获取字体图标
                choices=get_font()
            )
        }

