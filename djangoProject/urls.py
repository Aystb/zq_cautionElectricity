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
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

import users.views as users
from items import views as items

# 生成对Item增删改查的路由集
toItemRouter = DefaultRouter()
toItemRouter.register('items', items.ItemViewSet)

# 生成swagger文档
schema_view = get_schema_view(
    openapi.Info(
        title="cautionelectricity",
        default_version="v1",
        description="cautionelectricity",
        # 指定API的服务条款URL
        terms_of_service="API 遵循 REST标准进行设计。我们的 API是可预期的以及面向资源的",
        contact=openapi.Contact(email="3135287831@qq.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # 这里要调整权限
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/users', users.userIndex),
    path('index/items', items.itemIndex),
    # 获取单个项目
    re_path('cautionelectricity/(\d+)/items/getItem', users.getItem),
    # 获取所有项目
    re_path('cautionelectricity/(\d+)/allItems', users.getItems),
    # Router会自动生成获取所有项目、获取单个项目、修改单个项目，增加单个项目，删除单个项目的url
    re_path(r'^', include(toItemRouter.urls)),
    # 获取电量
    re_path('cautionelectricity/(\d+)/quantity', users.getElectricity),
    # 获取所有已完成项目
    re_path('cautionelectricity/(\d+)/completedItems', users.getcompleteItems),
    # 获取总结
    re_path('cautionelectricity/(\d+)/summarize', users.getsummary),
    # 修改指定项目
    re_path('cautionelectricity/(\d+)/items/modify', users.modifyItem),
    # 删除指定项目
    re_path('cautionelectricity/(\d+)/items/delete', users.deleteItem),
    # 新建项目
    re_path(r'cautionelectricity/(\d+)/items/create', items.createItem),
    # 新建用户
    path('cautionelectricity/createuser', users.createUser),
    # 登陆
    path('cautionelectricity/login', users.login),
    # 获取JwtToken
    re_path(r'cautionelectricity/(\d+)/getJwtToken', users.getJwtToken),
    # 获取token
    re_path(r'cautionelectricity/(\d+)/getToken', users.getToken),
    # 获取用户详细信息(解密版，可忽略)
    path('cautionelectricity/baseGetUserData', users.baseGetUserData),
    # 获取用户详细信息
    re_path(r'cautionelectricity/(\d+)/getUserData', users.getUserData),
    # 修改用户详细信息
    re_path(r'cautionelectricity/(\d+)/modifyUserData', users.changeUserData),
    # swagger文档路由
    path("cautionelectricity/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    # 完成项目
    re_path(r'cautionelectricity/(\d+)/completeItem', users.completeItem),
    # 账号密码登陆
    path('cautionelectricity/login_nameAndPassword', users.login_nameAndPassword),
    # 注册账号
    path('cautionelectricity/sign_up', users.sign_up)
]
