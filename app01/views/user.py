from django.shortcuts import render,HttpResponse,redirect
from app01.models import UserInfo,Department,MobileAccount
from django.utils.safestring import mark_safe
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from django import forms
from django import forms
from django.core.validators import RegexValidator #引入正则表达狮方法
from django.core.validators import ValidationError#引入错误提示返回方法
from app01.utils.form import UserModelForm,MobileModelForm,MobileEditModelForm
import copy

#用户列表页面
def user_list(request):
    queryset=UserInfo.objects.all()

    page_object=Pagination(request,queryset)
    page_queryset=page_object.page_queryset
    page_data=page_object.html()
    content={"data_list":page_queryset,
             "page_data":page_data,
             "user_active":"active"
             }
    return render(request, "user_list.html", content)
def user_add(request):
    if request.method=="GET":
        return render(request, "user_add.html")
    name= request.POST.get("name")
    password=request.POST.get("password")
    age = request.POST.get("age")
    mobile=request.POST.get("mobile")
    print(name,password,age)
    UserInfo.objects.create(name=name,password=password,age=age,mobile=mobile)
    return redirect("/user/list/")
"""#######用户删除#######"""
def user_delect(request):
    id=request.GET.get("nid")
    UserInfo.objects.filter(id=id).delete()
    return redirect("/user/list/")
#部门列表
def user_add_model(request):
    """用户新增，通过Model形式进行增加"""
    if request.method=="GET":
        #通过示例化，将拿到From信息
        form=UserModelForm()
        #返回界面，并将Form获取到内容，返回到界面
        return render(request, "user_add_model.html", {"form":form})
    form=UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        #通过form，直接保存到数据库
        form.save()
        return redirect("/user/list/")
    #print(form.errors)
    return render(request, "user_add_model.html", {"form":form})

def user_edit_model(request,nid):
    """通过modelform模式进行编辑用户信息"""
    #根据ID获取当前数据
    data_object = UserInfo.objects.filter(id=nid).first()
    if request.method=="GET":
        #根据传入的nid查询对应的数据
        #--data_object=UserInfo.objects.filter(id=nid).first()
        #将查询到到数据，设置为intance=获取到的对象
        form = UserModelForm(instance=data_object)
        return render(request, "user_edit_model.html", {"form":form})
    #获取界面的传值，并获取id的某一行数据，表示对指定对一条数据进行编辑
    form=UserModelForm(data=request.POST,instance=data_object)
    if form.is_valid():
        #若同时保存，非用户输入的信息，则可以通过如下方法
        #form.instance.字段名称=""
        form.save()
        return redirect("/user/list/")
    return render(request, "user_edit_model.html", {"form":form})