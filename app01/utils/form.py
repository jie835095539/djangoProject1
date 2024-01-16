"""定义一个自己到类，并继承forms.ModelForm"""
from django.shortcuts import render,HttpResponse,redirect
from app01.models import UserInfo,Department,MobileAccount
from django.utils.safestring import mark_safe
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from django import forms
from django import forms
from django.core.validators import RegexValidator #引入正则表达狮方法
from django.core.validators import ValidationError#引入错误提示返回方法
# ################## ModelForm 新增###########################3

class UserModelForm(forms.ModelForm):
    #重新定义name校验条件，validators=正则表达计算公式
    name=forms.CharField(min_length=3)
    class Meta:
        #通过form，获取用户信息
        model= UserInfo
        fields=["name","password","age","mobile","gender","depart","account","create_time"]
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"})
        }
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            print(name,field)
            field.widget.attrs={"class":"form-control"}


"""手机号增加表单设计"""
class MobileModelForm(BootStrapModelForm):
    mobile=forms.CharField(
        label="手机号码",
        validators=[RegexValidator(r'^1\d{10}$','手机号格式错误')]
    )
    class Meta:
        model = MobileAccount
        fields=["mobile","price","level","status"]
    #勾子方法，进行校验数据；；；；
    def clean_mobile(self):
        tex_mobile=self.cleaned_data["mobile"]
        exite=MobileAccount.objects.filter(mobile=tex_mobile,isdelect=0).exists()
        if exite:
            raise ValidationError("手机号重复")
        return tex_mobile

"""靓号管理编辑单独使用的modelform"""
class MobileEditModelForm(forms.ModelForm):
    mobile=forms.CharField(
        label="手机号码",
        validators=[RegexValidator(r'^1\d{10}$','手机号格式错误')],
        disabled=True#重新定义mobile属性，并将模板返回时，属性设置为不可以编辑；
    )
    class Meta:
        model = MobileAccount
        fields=["mobile","price","level","status"]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            print(name,field)
            field.widget.attrs={"class":"form-control"}
    #勾子方法，进行校验数据；；；；
    """def clean_mobile(self):
        tex_mobile=self.cleaned_data["mobile"]
        exite=MobileAccount.objects.filter(mobile=tex_mobile,isdelect=0).count()
        if exite>1:
            raise ValidationError("手机号重复")
        return tex_mobile"""

    def clean_mobile(self):
        tex_mobile = self.cleaned_data["mobile"]
        id=self.instance.pk#获取当前编辑的数据的id
        exite = MobileAccount.objects.exclude(id=id).filter(mobile=tex_mobile, isdelect=0).exists()
        if exite:
            raise ValidationError("手机号重复")
        return tex_mobile
class BootStrapForm:
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs["class"]="form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                #print(name,field)
                field.widget.attrs={"class":"form-control",
                                    "placeholder":field.label}