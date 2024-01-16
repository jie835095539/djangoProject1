from django.shortcuts import render,redirect,HttpResponse
from django import forms
import json
from django.views.decorators.csrf import csrf_exempt #引入这个方法，取消提交时，csrf的校验

from app01.models import Task
from app01.utils.form import BootStrapModelForm
from app01.utils.pagination import Pagination#分页方法



class TaskModelForm(BootStrapModelForm):

    class Meta:
        model = Task
        fields="__all__"
        widgets = {
            "remark": forms.TextInput
        }


def task_list(request):
    """任务列表"""
    #创建任务的表单方法
    form =TaskModelForm

    #查询数据并返回数据的方法
    #定义一个查询条件的字段
    select_data = {}
    data_list = Task.objects.filter(**select_data).order_by("id")
    #数据分页处理
    page_object = Pagination(request, data_list)
    #返回分页的数据
    page_queryset = page_object.page_queryset
    #返回分页界面代码
    page_data = page_object.html()
    context={"form":form,
             "page_queryset":page_queryset,
             "page_data":page_data}

    return render(request,"task_list.html",context)

@csrf_exempt
def task_add(request):
    """任务新建"""
    form=TaskModelForm(data=request.POST)
    if form.is_valid():
        #保存数据
        form.save()
        data_dict = {"status": True}
        # 通过这个字典进行dumps一下，返回前端
        json_data = json.dumps(data_dict)
        return HttpResponse(json_data)
    data_dict = {"status": False, "error": form.errors}
    # 通过这个字典进行dumps一下，返回前端
    json_data = json.dumps(data_dict)
    return HttpResponse(json_data)

@csrf_exempt
def task_add_test(request):
    # 获取到一个数据字典
    data_dict = {"status": True, "data": [11, 22, 33, 44]}
    # 通过这个字典进行dumps一下，返回前端
    json_data = json.dumps(data_dict)
    return HttpResponse(json_data)
