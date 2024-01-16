from django.shortcuts import render,HttpResponse,redirect
from app01.models import UserInfo,Department,MobileAccount,Admin
from django.utils.safestring import mark_safe
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5
from app01.utils.imgcode import check_code

from io import BytesIO
from django import forms
from django import forms
from django.core.validators import RegexValidator #引入正则表达狮方法
from django.core.validators import ValidationError#引入错误提示返回方法
from app01.utils.form import UserModelForm,MobileModelForm,MobileEditModelForm
import copy


from app01.utils import form

class login(forms.Form,form.BootStrapForm):
    """定义登录界面字段Form表单"""
    account=forms.CharField(label="用户名",
                         widget=forms.TextInput(attrs={"class":"form-control"}),
                         required=True
                         )
    password=forms.CharField(label="密码",
                             widget=forms.PasswordInput(attrs={"class":"form-control"}),
                             required=True)
    code=forms.CharField(label="验证码",
                         widget=forms.TextInput(attrs={"class": "form-control"}),
                         required=True
                         )
    def clean_password(self):
        """针对界面获取的密码，进行MD5加密处理，处理完成后返回加密的密码，用于登录密码的校验"""
        pwd=self.cleaned_data.get("password")
        print(pwd)
        return md5(pwd)

def new_login(request):
    """登录处理方法"""
    if request.method=="GET":
        form=login()
        return render(request,"new_login.html",{"form":form})
    #获取登录，输入的信息；
    form=login(data=request.POST)
    #判断输入的信息是否存在，如果存在则继续
    if form.is_valid():
        #1、从用户输入到信息中，将输入的code取出来，取出来后方便后面查询用户
        user_input_code=form.cleaned_data.pop("code")
        print("用户输入的验证码",user_input_code)
        # 从缓存中取到当前用户session中保存的图片验证码文本，校验与用户输入是否一致
        img_code=request.session.get("image_code")
        print("缓存验证码", img_code)
        #校验验证，用户输入的是否一致
        if str(user_input_code).lower() !=str(img_code).lower():
            #不一致，返回验证码不一致
            form.add_error("code","验证码不正确")
            #并返回登录界面
            return render(request, "new_login.html", {"form": form})
        #print(user_input_code)
        # 根据界面输入的条件，查询数据库，获取数据库的用户信息
        value=Admin.objects.filter(**form.cleaned_data).first()
        print("数据", not value)
        # 如果用户信息不存在
        if not value:
            #增加错误信息，到界面输入到字段属性中
            form.add_error("password", "账户密码错误")
            #并返回登录界面
            return render(request, "new_login.html", {"form": form})
        #如果存在值
        else:
            #将当前用户到session进行保存
            request.session["info"]={"username":value.username,"id":value.id,"account":value.account}
            #设置session失效时间，60*60秒
            request.session.set_expiry(60*60*24*7)
            #并直接重新定向跳转到对应界面
            return redirect("/index/")
        print(form.cleaned_data)
    # 判断输入的信息是否存在，如果存在则继续
    return render(request, "new_login.html", {"form": form})

def out_login(request):
    """账户注销登录方法"""
    #清除当前用户session信息
    request.session.clear()
    #怎么总是忘记，return
    return redirect("/login/new/")


def image_code(request):
    """获取验证码"""
    # 1.通过验证码生成方法，获取验证码，验证码函数，返回验证码、及其验证码文字
    img,code=check_code()
    #将获取到的验证码文本信息，写入到session中，用于后期验证码到验证
    request.session["image_code"]=code
    request.session.set_expiry(60)
    # 2. 写入内存(Python3)
    stream = BytesIO()
    img.save(stream, 'png')
    #2.从内存中获取图片并返回
    return HttpResponse(stream.getvalue())