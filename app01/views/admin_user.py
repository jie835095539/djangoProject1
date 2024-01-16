import copy

from django.shortcuts import redirect,render,HttpResponse
from django.utils.safestring import mark_safe
from django import forms
from django.core.validators import RegexValidator #引入正则表达狮方法
from django.core.validators import ValidationError#引入错误提示返回方法

from app01.models import Admin
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5
from app01.utils.form import UserModelForm,MobileModelForm,MobileEditModelForm


def admin_list(request):
    """管理员列表"""
    #搜索
    search_data={}
    username=request.GET.get("username","")
    if username:
        search_data["username__contains"]=str(username)
    form_data = Admin.objects.filter(**search_data)
    #分页
    page_object=Pagination(request,form_data)
    page_form_data=page_object.page_queryset
    page_string=page_object.html()

    context={
        "username":username,
        "form_data":page_form_data,
        "page_string":page_string,
        "admin_active":"active"

    }
    return render(request,"admin_list.html",context)

class AdminModelForm(BootStrapModelForm):
    """管理员新增Modelform"""
    confirm_password=forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)#更高字段属性，方式一
    )
    class Meta:
        model=Admin
        fields=["username","account","password","confirm_password"]
        widgets={
            "password":forms.PasswordInput(render_value=True)#更改字段属性，方式二
        }
    def clean_password(self):
        pwd=self.cleaned_data.get("password")
        return md5(str(pwd))
    def clean_username(self):
        tex_username = self.cleaned_data["username"]
        id=self.instance.pk#获取当前编辑的数据的id
        #排除自己，查看是否存在
        exite = Admin.objects.exclude(id=id).filter(username=tex_username).exists()
        if exite:
            raise ValidationError("用户已经存在")
        return tex_username

    #通过勾子方法，进行密码校验，校验是否一直，校验完成，结果会保存到form中
    def clean_confirm_password(self):
        pwd= self.cleaned_data.get("password")
        confrm=md5(self.cleaned_data.get("confirm_password"))
        if pwd != confrm:
            raise ValidationError("密码不一致")
        return confrm


def admin_add(request):
    title="管理员新增"
    if request.method=="GET":
        form = AdminModelForm()
        return render(request,"modelform_add.html",{
        "title": title,
        "form": form
    })
    #通过这个类接收一下，用户提交的数据
    form=AdminModelForm(data=request.POST)
    #直接保存数据
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "modelform_add.html", {
        "title": title,
        "form": form
    })
    """管理员添加"""

def admin_delect(request,nid):
    """管理员删除"""
    Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")

class AdminEditModelForm(BootStrapModelForm):
    """管理员编辑Modelform"""
    class Meta:
        model=Admin
        fields=["username"]
        widgets={
            "password":forms.PasswordInput(render_value=True)#更改字段属性，方式二
        }
    def clean_password(self):
        pwd=self.cleaned_data.get("password")
        return md5(str(pwd))

    #通过勾子方法，进行密码校验，校验是否一直，校验完成，结果会保存到form中
    def clean_confirm_password(self):
        pwd= self.cleaned_data.get("password")
        confrm=md5(self.cleaned_data.get("confirm_password"))
        if pwd != confrm:
            raise ValidationError("密码不一致")
        return confrm

def admin_edit(request,nid):
    """管理员编辑"""
    title="管理员编辑"+"--"+Admin.objects.filter(id=nid).first().username
    obj=Admin.objects.filter(id=nid).first()
    if request.method=="GET":
        form = AdminEditModelForm(instance=obj)
        return render(request,"modelform_add.html",{"form":form,"title":title})
    form=AdminEditModelForm(data=request.POST,instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")

    return render(request, "modelform_add.html", {"form": form, "title": title})


class AdminResetModelForm(BootStrapModelForm):
    """管理员重置密码"""
    confirm_password=forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)#更高字段属性，方式一
    )
    class Meta:
        model=Admin
        fields=["password","confirm_password"]
        widgets={
            "password":forms.PasswordInput(render_value=True)#更改字段属性，方式二
        }
    def clean_password(self):
        pwd=self.cleaned_data.get("password")
        return md5(str(pwd))

    #通过勾子方法，进行密码校验，校验是否一直，校验完成，结果会保存到form中
    def clean_confirm_password(self):
        pwd= self.cleaned_data.get("password")
        confrm=md5(self.cleaned_data.get("confirm_password"))
        if pwd != confrm:
            raise ValidationError("密码不一致")
        return confrm


def admin_reset(request,nid):
    obj = Admin.objects.filter(id=nid).first()
    title = "密码重置" + "--" + obj.username
    if request.method=="GET":
        form =AdminResetModelForm()
        return render(request,"modelform_add.html",{"form":form,"title":title})
    form=AdminResetModelForm(data=request.POST,instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "modelform_add.html", {"form": form, "title": title})

