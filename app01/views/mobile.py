from django.shortcuts import render,HttpResponse,redirect
from app01.models import UserInfo,Department,MobileAccount
from django.utils.safestring import mark_safe
from app01.utils.pagination import Pagination#分页方法
from app01.utils.bootstrap import BootStrapModelForm
from django import forms
from django import forms
from django.core.validators import RegexValidator #引入正则表达狮方法
from django.core.validators import ValidationError#引入错误提示返回方法
from app01.utils.form import UserModelForm,MobileModelForm,MobileEditModelForm
import copy


def mobile_list(request):
    """靓号列表"""
    if request.method=="GET":
        mobile=request.GET.get("mobile","")
        select_data = {"isdelect": 0}
        if mobile:
            select_data["mobile__contains"]=str(mobile)#界面有查询条件，则进行拼装查询条件
        data_list = MobileAccount.objects.filter(**select_data).order_by("-level")

        #分页展示
        page_object = Pagination(request, data_list)
        page_queryset = page_object.page_queryset
        page_data = page_object.html()
        content={
                 "select_data": mobile,
                "data_obj": page_queryset,
                     "page_data":page_data,
            "mobile_active":"active"
        }
        return render(request, "mobile_list.html", content)

def mobile_add(request):
    if request.method=="GET":
        form=MobileModelForm()
        return render(request, "mobile_add.html", {"form":form})
    form=MobileModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/mobile/list/")
    return render(request, "mobile_add.html", {"form":form})


def mobile_edit(request,nid):
    """靓号编辑工作"""
    data_list = MobileAccount.objects.filter(id=nid).first()
    if request.method=="GET":
        form=MobileEditModelForm(instance=data_list)
        return render(request, "mobile_edit.html", {"form":form})
    form=MobileEditModelForm(data=request.POST,instance=data_list)
    if form.is_valid():
        form.save()
        return redirect("/mobile/list/")
    return render(request, "mobile_add.html", {"form":form})

def mobile_delect(request,nid):
    """逻辑删除手机号"""
    MobileAccount.objects.filter(id=nid).update(isdelect=1)
    return redirect('/mobile/list/')
