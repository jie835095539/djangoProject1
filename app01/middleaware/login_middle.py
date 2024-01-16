from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect,render

class test(MiddlewareMixin):
    #函数名称：process_request,固定的，其他名称不起作用
    def process_request(self, request):
        print("请求来了")
        return HttpResponse("nihao")

    # 函数名称：process_response,固定的，其他名称不起作用
    def process_response(self, request, response):
        print("请求来了")
        return response

class login_account(MiddlewareMixin):

    def process_request(self,request):
        #需要排除登录界面，将登录界面不校验session
        #request.path_info,获取当前用户登录的url,request.path_info=="/login/new/"
        if request.path_info in ["/login/new/","/image/code/"]:
            return
        # 读取当前用户session信息，判断是否已经登录
        session_dict=request.session.get("info")
        #如果存在，则返回none
        if session_dict:
            return
        print("请求来了")
        # 如果不存在，则返回登录界面
        return redirect("/login/new/")

