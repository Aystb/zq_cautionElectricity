import base64
import json
from Cryptodome.Cipher import AES
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import resolve
import datetime

from users.models import User
from items.models import Item
from jwt_auth import jwt_auth


# Create your views here.
def userIndex(request):
    return HttpResponse("users!")


# 新建用户
# 已弃用
def createUser(request):
    name = request.POST['name']
    password = request.POST['password']
    User.objects.create(name=name, password=password, electricity=100, completedItems=0, shutDownCount=0)
    return HttpResponse("createUser")


# 根据用户id获取电量
def getElectricity(request, userid):
    data = User.objects.filter(id=userid)
    print(data[0].electricity)
    return JsonResponse(data[0].electricity, safe=False)


# 获取单个项目
def getItem(request, userid):
    data = User.objects.filter(id=userid)
    itemDatas = data[0].item_set.all()
    # 这里用data2[0].name可以但是用request.GET的不行，初步估计是数据类型的问题,现在找到问题，filter中的数据必须是一个元组类型
    # 如果是itemName需要加一层括号将它变成元组,也就是写成(request.GET['itemName'],)而不是request.GET['itemName']
    # 发现是创建项目的时候引起的bug，会把括号也加入到项目名字，变成（‘it’，），引以为戒
    itemName = request.GET['itemName']
    # itemData=data2.filter(name=data2[1].name)
    itemData = itemDatas.filter(name=itemName)
    jsonData = {
        "itemName": itemData[0].name,
        "ddl": itemData[0].ddl,
        "electricityConsume": itemData[0].electricityConsume,
        "details": itemData[0].details,
    }
    return JsonResponse(jsonData, safe=False)


# 获取所有项目
def getItems(request, userid):
    userDatas = User.objects.filter(id=userid)
    itemDatas = userDatas[0].item_set.filter(isCompleted=0)
    jsonData = [{
        "itemName": item.name,
        "ddl": item.ddl,
        "electricityConsume": item.electricityConsume,
        "details": item.details,
    } for item in itemDatas]
    return JsonResponse(jsonData, safe=False)


# 获取所有已完成的项目
def getcompleteItems(request, userid):
    userData = User.objects.filter(id=userid)
    completed_items = userData[0].item_set.filter(isCompleted=True)
    jsonData = [{
        "itemName": item.name,
        "ddl": item.ddl,
        "electricityConsume": item.electricityConsume,
        "details": item.details,
    } for item in completed_items]
    return JsonResponse(jsonData, safe=False)


def get_get_data(url):
    response = requests.get(url)
    data = response.json()
    return data


# 目前使用的是自己的appid，secret，后续需要更新成前端那边的
def login(request):
    code = request.GET["code"]
    print(code)
    url = "https://api.weixin.qq.com/sns/jscode2session" + "?appid=wxcced61f7c6355283&secret=975d9ab132a37f040b476f4571490d00&js_code=" + code + "&grant_type=authorization_code"
    loginData = get_get_data(url)
    print(loginData)
    newSession_key = (loginData['session_key'],)
    newOpenid = (loginData['openid'],)
    # 首先在数据库里面寻找openid
    user = User.objects.filter(openid=newOpenid)
    if (user.exists()):
        # print(user[0].id)
        return JsonResponse(user[0].id, safe=False)
    # 如果没有则创建新用户
    else:
        User.objects.create(name='', password=123456, electricity=100, completedItems=0, shutDownCount=0,
                            openid=newOpenid, session_key=newSession_key)
        nowUser = User.objects.filter(openid=newOpenid)
        return JsonResponse(nowUser[0].id, safe=False)


def getJwtToken(request, userid):
    userData = User.objects.filter(id=userid)
    openid = userData[0].openid
    newJwtToken = jwt_auth.create_jwtToken(openid)
    # 获取到jwtToken后立马验证试试
    print(newJwtToken)
    Message = jwt_auth.identify_token(newJwtToken)
    # payload中的信息
    print(Message)
    userData.update(token=newJwtToken)
    return JsonResponse(newJwtToken, safe=False)


def getToken(request, userid):
    userData = User.objects.filter(id=userid)
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxcced61f7c6355283&secret=975d9ab132a37f040b476f4571490d00"
    newToken = get_get_data(url)
    return JsonResponse(newToken, safe=False)


def baseGetUserData(request, session_key):
    postBody = request.body
    json_result = json.loads(postBody)
    data = json_result['code']
    data = json.loads(data)
    encryptedData = data['encryptedData']
    iv = data['iv']
    jsonData = decrypt_user_info(encryptedData, session_key, iv)
    print(jsonData)
    return JsonResponse(jsonData, safe=False)


def decrypt_user_info(encrypted_data, session_key, iv):
    def get_decrypt_data(encrypted_data, session_key, iv):
        session_key = base64.b64decode(session_key)
        encrypted_data = base64.b64decode(encrypted_data)
        iv = base64.b64decode(iv)
        cipher = AES.new(session_key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(encrypted_data)
        decrypted_data = decrypted_data[:-decrypted_data[-1]].decode('utf-8')
        return decrypted_data

    decrypted_data = get_decrypt_data(encrypted_data, session_key, iv)
    user_info = json.loads(decrypted_data)
    return user_info


def getsummary(request, userid):
    userData = User.objects.filter(id=userid)
    summary = {
        'name': userData[0].name,
        'shut_down_count': userData[0].shutDownCount,
        'completed_items': userData[0].completedItems
    }
    return JsonResponse(summary)


def modifyItem(request, userid, ):
    itemName = request.GET['itemName']
    userDatas = User.objects.filter(id=userid)
    item = userDatas[0].item_set.filter(name=itemName)
    new_item_name = request.POST.get('itemName')
    new_ddl = request.POST.get('ddl')
    new_electricityConsume = request.POST.get('electricityConsume')
    new_details = request.POST.get('details')
    if (new_electricityConsume):
        item.update(electricityConsume=new_electricityConsume)
    if (new_item_name):
        item.update(name=new_item_name)
    if (new_details):
        item.update(details=new_details)
    if (new_ddl):
        item.update(ddl=new_ddl)

    return HttpResponse("Item information updated successfully")


def deleteItem(request, userid):
    itemName = request.GET['itemName']
    userDatas = User.objects.filter(id=userid)
    userDatas[0].item_set.filter(name=itemName).delete()
    return HttpResponse("Item deleted successfully")


def getUserData(request, userid):
    userDatas = User.objects.filter(id=userid)
    name = userDatas[0].name
    password = userDatas[0].password
    electricity = userDatas[0].electricity
    completed_items = userDatas[0].completedItems
    shutdown_count = userDatas[0].shutDownCount
    return JsonResponse({
        'name': name,
        'password': password,
        'electricity': electricity,
        'completed_items': completed_items,
        'shutdown_count': shutdown_count,
    })


def changeUserData(request, userid):
    userDatas = User.objects.filter(id=userid)
    new_name = request.POST.get('name')
    new_password = request.POST.get('password')
    new_electricity = request.POST.get('electricity')
    new_completed_items = request.POST.get('completedItems')
    new_shutdown_count = request.POST.get('shutDownCount')
    oldName = User.objects.filter(name=new_name)
    if (new_name and not oldName.exists()):
        userDatas.update(name=new_name)
    if (new_password):
        userDatas.update(password=new_password)
    if (new_electricity):
        userDatas.update(electricity=new_electricity)
    if (new_completed_items):
        userDatas.update(completedItems=new_completed_items)
    if (new_shutdown_count):
        userDatas.update(shutDownCount=new_shutdown_count)
    return HttpResponse("User information updated successfully")


def completeItem(request, userid):
    postBody = request.body
    json_result = json.loads(postBody)
    data = User.objects.filter(id=userid)
    itemDatas = data[0].item_set.all()
    itemName = (json_result['itemName'],)
    itemData = itemDatas.filter(name=itemName[0])
    # 注意，这里要用update方法才能更新，千万不能用itemData[0].isCompleted=1这种方式赋值
    itemData.update(isCompleted=True)
    return HttpResponse("successfully updated")


def login_nameAndPassword(request):
    iname = request.GET['name']
    ipassword = request.GET['password']
    name = User.objects.filter(name=iname);
    # 如果存在用户名则查找密码是否符合，否则返回用户名不存在
    if (not name.exists()):
        jsonData = "该用户名还未注册"
        return JsonResponse(jsonData, safe=False)
    password = User.objects.filter(password=ipassword)
    if (not password.exists()):
        jsonData = "密码错误"
        return JsonResponse(jsonData, safe=False)
    userData = User.objects.filter(name=iname)
    id = userData[0].id
    return JsonResponse(id, safe=False)


def sign_up(request):
    postBody = request.body
    json_result = json.loads(postBody)
    name = json_result['name']
    oldName = User.objects.filter(name=name)
    if (oldName.exists()):
        return HttpResponse("当前用户名已存在")
    password = json_result['password']
    User.objects.create(name=name, password=password, electricity=100, completedItems=0, shutDownCount=0)
    userData = User.objects.filter(name=name)
    id = userData[0].id
    return JsonResponse(id, safe=False)
