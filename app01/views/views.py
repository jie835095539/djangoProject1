from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt #引入这个方法，取消提交时，csrf的校验
import json
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
# Create your views here.
#函数首页
def index(request):
    return render(request,"index.html")
def tpl(request):
    name="张英东"
    roles=["管理员","CEO","操作员"]
    user_info={"name":"zyd","old":13,"salary":10000,"role":"CTO"}
    return render(request, "tpl.html", {"n1":name, "n2":roles, "n3":user_info})
def news(request):
    import requests
    headers={
      "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    url="https://www.chinaunicom.com.cn/api/article/NewsByIndex/2/2023/12/news"
    data_list=requests.get(url,headers=headers).json()
    print(data_list)
    return render(request, "news.html", {"news":data_list})
#定义请求与响应
def something(request):
    #打印界面请求方式：GET/POST
    print(request.method)
    #获取界面请求参数
    data=request.GET
    #打印界面请求参数
    print(data)
    #第一种响应方式
    return HttpResponse("返回文字响应")
    #第二种响应方式
    #return render(request,"something.html")
    #第三种响应方式
    #return redirect("https://www.baidu.com")
#用户登录案例
def login(request):
    #若请求为GET方式，则返回login界面
    if request.method=="GET":
        #print(request.method)
        return redirect("/login/new/")
    #如果不是GET请求，则继续执行
    print(request.POST)
    #获取界面请求参数
    usrname=request.POST.get("user","")
    password=request.POST.get("psw","")
    print(usrname,password)
    #校验输入的账号密码，校验成功，则执行跳转
    if usrname=="admin" and password=="123456":
        #return HttpResponse("提交成功")
        return redirect("/index/")
   # return HttpResponse("提交失败")
    #校验失败，则提示密码不正确
    return render(request, "login.html", {"error_msg": "用户名称或密码错误","user":usrname,"psw":password})
"""#######用户增加#######"""



def xiaomi(request):
    return render(request,"xiaomi.html")


def text_ajax(request):
    return render(request,"test_ajax.html")


@csrf_exempt
def text_sub(request):

    data=request.GET.get("name")
    print(data)
    #获取到一个数据字典
    data_dict={"status":True,"data":[11,22,33,44]}
    # 通过这个字典进行dumps一下，返回前端
    json_data=json.dumps(data_dict)
    return HttpResponse(json_data)






