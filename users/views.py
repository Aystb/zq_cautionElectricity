from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from users.models import User
from items.models import Item


# Create your views here.
def index(request):
    return HttpResponse("users!")


def getItem(request):
    print(request.method)
    print(request.GET)
    name = request.GET['项目名称']
    print(name)
    return HttpResponse("getItem")


# 新建用户
def createUser(request):
    name = request.POST['name']
    password = request.POST['password']
    User.objects.create(name=name, password=password, electricity=100, completedItems=0, shutDownCount=0)
    return HttpResponse("createUser")


# 根据用户id获取电量
def getElectricity(request, userid):
    data = User.objects.filter(id=userid)
    return JsonResponse(data[0].electricity, safe=False)


# 获取单个项目
def getItem(request, userid):
    data = User.objects.filter(id=userid)
    itemDatas = data[0].item_set.all()
    # 这里用data2[0].name可以但是用request.GET的不行，初步估计是数据类型的问题,现在找到问题，filter中的数据必须是一个元组类型
    # 如果是itemName需要加一层括号将它变成元组,也就是写成(request.GET['itemname'],)而不是request.GET['itemname']
    itemName = (request.GET['itemname'],)
    # itemData=data2.filter(name=data2[1].name)
    itemData = itemDatas.filter(name=itemName)
    jsonData = {
        "项目名称": itemData[0].name,
        "截止日期": itemData[0].ddl,
        "消耗电量": itemData[0].electricityConsume,
        "具体内容": itemData[0].details,
    }
    return JsonResponse(jsonData, safe=False)


# 获取所有项目
def getItems(request, userid):
    userDatas = User.objects.filter(id=userid)
    itemDatas = userDatas[0].item_set.filter(isCompleted=0)
    jsonData = [{
        "项目名称": item.name,
        "截止日期": item.ddl,
        "消耗电量": item.electricityConsume,
        "具体内容": item.details,
    } for item in itemDatas]
    return JsonResponse(jsonData, safe=False)
