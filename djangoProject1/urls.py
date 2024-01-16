"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views import views,user,depart,mobile,admin_user,login,task,order
urlpatterns = [
    path("index/",views.index),
    path("user/list/",user.user_list),
    path("tpl/",views.tpl),
    path("news/",views.news),
    path("something/",views.something),
    path("login/",views.login),
    path("user/add/",user.user_add),
    path("user/add/model/",user.user_add_model),
    path("user/edit/<int:nid>/model/",user.user_edit_model),
    path("user/delect/",user.user_delect),
    path("depart/list/",depart.depart_list),
    path("depart/add/",depart.depart_add),
    path("depart/delect/",depart.depart_delect),
    path("depart/<int:nid>/edit/",depart.depart_edit),
    path("mobile/list/",mobile.mobile_list),
    path("mobile/add/", mobile.mobile_add),
    path("mobile/<int:nid>/edit/",mobile.mobile_edit),
    path("mobile/<int:nid>/delect/",mobile.mobile_delect),
    #管理员
    path("admin/list/",admin_user.admin_list),
    path("admin/add/",admin_user.admin_add),
    path("admin/<int:nid>/edit/",admin_user.admin_edit),
    path("admin/<int:nid>/delect/",admin_user.admin_delect),
    path("admin/<int:nid>/reset/", admin_user.admin_reset),
    path("xiaomi/",views.xiaomi),
    path("login/new/",login.new_login),
    path("login/out/",login.out_login),
    path("image/code/",login.image_code),

    #ajax发送请求测试案例
    path("test/ajax/",views.text_ajax),
    path("test/sub/",views.text_sub),

    #任务列表
    path("task/list/", task.task_list),
    path("task/add/",task.task_add),
    path("task/add/test/",task.task_add_test),

    #订单列表
    path("order/list/",order.order_list),
    path("order/add/",order.order_add)


]