"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path
from items import views as items
from users import views as users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/users', users.index),
    path('index/items', items.index),
    # 获取单个项目
    re_path('m1/4020303-0-default/cautionelectricity/(\d+)/items', users.getItem),
    # 获取所有项目
    re_path('m1/4020303-0-default/cautionelectricity/(\d+)/allItems', users.getItems),
    # 获取电量
    re_path('m1/4020303-0-default//cautionelectricity/(\d+)/quantity', users.getElectricity),
    # 获取所有已完成项目
    re_path('m1/4020303-0-default/cautionelectricity/(\d+)/allcomplishItems', users.getcompleteItems),
    # 获取总结
    path('m1/4020303-0-default/cautionelectricity/getsummary', users.getsummary),
    # 修改指定项目
    path('m1/4020303-0-default/cautionelectricity/changeitem', users.changeitem),
    # 删除指定项目
    path('m1/4020303-0-default/cautionelectricity/deleteitem', users.deleteitem),
    # 新建项目
    re_path(r'm1/4020303-0-default/cautionelectricity/(\d+)/items/create', items.createItem),
    # 新建用户
    path('m1/4020303-0-default/cautionelectricity/createuser', users.createUser),
    # 登陆
    path('m1/4020303-0-default/cautionelectricity/login', users.login),
    # 获取token
    re_path(r'm1/4020303-0-default/cautionelectricity/(\d+)/getToken', users.getToken),
    # 获取用户详细信息(解密版，可忽略)
    path('m1/4020303-0-default/cautionelectricity/getUserData', users.baseGetUserData),
    # 获取用户详细信息
    path('m1/4020303-0-default/cautionelectricity/getUserDataplus', users.getUserDataplus),
    # 修改用户详细信息
    path('m1/4020303-0-default/cautionelectricity/changeUserData', users.changeUserData),

]
