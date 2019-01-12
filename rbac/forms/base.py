from django import forms

class BaseModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        """
        统一给ModelForm字段构建样式
        :param args:
        :param kwargs:
        """
        super(BaseModelForm, self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'margin-top:10px'