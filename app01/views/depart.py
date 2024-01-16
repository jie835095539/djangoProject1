from django.shortcuts import render,HttpResponse,redirect
from app01.models import UserInfo,Department,MobileAccount
from django.utils.safestring import mark_safe
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from django import forms
from django.core.validators import RegexValidator #引入正则表达狮方法
from django.core.validators import ValidationError#引入错误提示返回方法
from app01.utils.form import UserModelForm,MobileModelForm,MobileEditModelForm
import copy

def depart_list(request):
    """部门列表"""
    if request.method=="GET":
        data_list=Department.objects.all()
        page_object = Pagination(request, data_list)
        page_queryset = page_object.page_queryset
        page_data = page_object.html()
        content = {"departs": page_queryset,
                   "page_data": page_data,
                   "depart_active":"active"
                   }

        return render(request, "depart_list.html", content)
#部门添加
def depart_add(request):
    """添加部门"""
    if request.method=="GET":
        return render(request, "depart_add.html")
    #获取用户POST形式提交的数据信息
    depart_name=request.POST.get("depart_name")#提交的部门名称
    company=request.POST.get("company")#提交的公司名称
    print(depart_name,company)#打印
    Department.objects.create(depart_name=depart_name,company=company)#数据库新增数据
    return redirect("/depart/list/")#添加完成数据，并进行重新定向界面
#部门删除
def depart_delect(request):
    """删除部门"""
    #获取要删除的数据的Id
    nid=request.GET.get("nid")
    print(nid)
    #根据id删除部门数据
    Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")
#部门编辑
def depart_edit(request,nid):#通过上一步骤，设置了链接传入参数后，方法中需要设置接收的参数nid（与链接维护添加参数的区别）
    """编辑部门数据"""
    if request.method=="GET":
        data_one=Department.objects.filter(id=nid).first()
        return render(request, "depart_edit.html", {"data_edit":data_one})
    depart_name = request.POST.get("depart_name")  # 提交的部门名称
    company = request.POST.get("company")  # 提交的公司名称
    print(depart_name, company)  # 打印
    Department.objects.filter(id=nid).update(depart_name=depart_name, company=company)  # 数据库新增数据
    return redirect("/depart/list/")  # 添加完成数据，并进行重新定向界面