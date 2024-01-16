import json
import random
from datetime import datetime
from django import forms
from django import forms
from django.core.validators import RegexValidator #引入正则表达狮方法
from django.core.validators import ValidationError#引入错误提示返回方法
from django.utils.safestring import mark_safe
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt #引入这个方法，取消提交时，csrf的校验

from app01.models import UserInfo,Department,MobileAccount,Order
from app01.utils.pagination import Pagination#分页方法
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.form import UserModelForm,MobileModelForm,MobileEditModelForm
from app01.utils.encrypt import makeid


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model=Order
        #可以重新定义显示字段，定义全部显示
        #fields="__all__"
        # 可以重新定义显示字段
        #fields=[]
        #定义显示字段，排除要显示的字段
        exclude=["oid","admin"]


def order_list(request):
    """任务列表"""
    # 创建任务的表单方法
    form=OrderModelForm()
    # 查询数据并返回数据的方法
    # 定义一个查询条件的字段
    select_data = {}
    data_list = Order.objects.filter(**select_data).order_by("-oid")
    # 数据分页处理
    page_object = Pagination(request, data_list)
    # 返回分页的数据
    page_queryset = page_object.page_queryset
    # 返回分页界面代码
    page_data = page_object.html()
    context = {"form": form,
               "page_queryset": page_queryset,
               "page_data": page_data}

    return render(request,"order_list.html",context)

@csrf_exempt
def order_add(request):
    form=OrderModelForm(data=request.POST)
    if form.is_valid():
        #当界面用户输入的字段信息不够时，可以给对应字段进行赋值，oid，进行赋值
        form.instance.oid=makeid(pr="JD",lg=7)
        #从session获取用户信息，并将用户信息设置到数据创建人
        form.instance.admin_id=request.session["info"]["id"]
        form.save()
        data_dict = {"status": True}
        # 通过这个字典进行dumps一下，返回前端
        json_data = json.dumps(data_dict)
        return HttpResponse(json_data)
    data_dict = {"status": False, "error": form.errors}
    # 通过这个字典进行dumps一下，返回前端
    json_data = json.dumps(data_dict)
    return HttpResponse(json_data)