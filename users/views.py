import base64
import json
from Cryptodome.Cipher import AES
import requests
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
    name = request.GET['itemName']
    print(name)
    return HttpResponse("getItem")


def createUser(request):
    name = request.POST['name']
    password = request.POST['password']
    User.objects.create(name=name, password=password, electricity=100, completedItems=0, shutDownCount=0)
    return HttpResponse("createUser")


def getElectricity(request, userid):
    data = User.objects.filter(id=userid)
    print(data[0].electricity)
    return JsonResponse(data[0].electricity, safe=False)


def getItem(request, userid):
    data = User.objects.filter(id=userid)
    itemDatas = data[0].item_set.all()
    # 这里用data2[0].name可以但是用request.GET的不行，初步估计是数据类型的问题,现在找到问题，filter中的数据必须是一个元组类型
    # 如果是itemName需要加一层括号将它变成元组,也就是写成(request.GET['itemname'],)而不是request.GET['itemname']
    itemName = (request.GET['itemname'],)
    # itemData=data2.filter(name=data2[1].name)
    itemData = itemDatas.filter(name=itemName)
    jsonData = {
        "itemName": itemData[0].name,
        "ddl": itemData[0].ddl,
        "electricityConsume": itemData[0].electricityConsume,
        "details": itemData[0].details,
    }
    return JsonResponse(jsonData, safe=False)


def getItems(request, userid):
    userDatas = User.objects.filter(id=userid)
    itemDatas = userDatas[0].item_set.filter(isCompleted=0)
    jsonData = [{
        "itemName": item.name,
        "ddl": item.ddl,
        "electricity": item.electricityConsume,
        "details": item.details,
    } for item in itemDatas]
    return JsonResponse(jsonData, safe=False)


def get_get_data(url):
    response = requests.get(url)
    data = response.json()
    return data


# 目前使用的是自己的appid，secret，后续需要更新成前端那边的
def login(request):
    code = request.GET["code"]
    url = "https://api.weixin.qq.com/sns/jscode2session" + "?appid=wxba92e34da68b5aeb&secret=dd74ff753006510da7ce0f5321d36dae&js_code=" + code + "&grant_type=authorization_code"
    loginData = get_get_data(url)
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


def getToken(request, userid):
    userData = User.objects.filter(id=userid)
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxba92e34da68b5aeb&secret=dd74ff753006510da7ce0f5321d36dae"
    newToken = get_get_data(url)
    print(newToken)
    userData.update(token=newToken)
    return JsonResponse(newToken, safe=False)


def baseGetUserData(request, session_key):
    data = request.GET['code']
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

def getcompleteItems(request,userid):
    userData = User.objects.filter(id=userid)
    completed_items = User.item_set.filter(completed=True)
    completed_items_data = []
    for item in completed_items:
        item_data = {
            "itemName": item.name,
            "ddl": item.ddl,
            "electricityConsume": item.electricityConsume,
            "details": item.details,
        }
    completed_items_data.append(item_data)
    return JsonResponse(completed_items_data, safe=False)

def getsummary(request,userid):
    userData = User.objects.filter(id=userid)
    summary = {
        'name': User.name,
        'shut_down_count': User.shutDownCount,
        'completed_items': User.completedItems
    }
    return JsonResponse(summary)

def changeitem(request,userid,itemname):
    userDatas = User.objects.filter(id=userid)
    item = User.item_set.filter(name=itemname)
    new_item_name = request.POST.get('itemName')
    new_ddl = request.POST.get('ddl')
    new_electricity = request.POST.get('electricity')
    new_details = request.POST.get('details')
    item.name = new_item_name
    item.ddl = new_ddl
    item.electricity = new_electricity
    item.details = new_details
    item.save()
    return HttpResponse("Item information updated successfully")
def deleteitem(request,userid,itemname):
    userDatas = User.objects.filter(id=userid)
    item = User.item_set.filter(name=itemname)
    item.delete()
    return HttpResponse("Item deleted successfully")

def getUserDataplus(request,userid):
    userDatas = User.objects.filter(id=userid)
    name = User.name
    password = User.password
    electricity = User.electricity
    completed_items = User.completed_items
    shutdown_count = User.shutdown_count
    return JsonResponse({
        'name': name,
        'password': password,
        'electricity': electricity,
        'completed_items': completed_items,
        'shutdown_count': shutdown_count,
    })

def changeUserData(request,userid):
    userDatas = User.objects.filter(id=userid)
    new_name = request.POST.get('Name')
    new_password = request.POST.get('password')
    new_electricity = request.POST.get('electricity')
    new_completed_items = request.POST.get('completedItems')
    new_shutdown_count = request.POST.get('shutDownCount')
    User.name = new_name
    User.password = new_password
    User.electricity = new_electricity
    User.completed_items = new_completed_items
    User.shutdown_count = new_shutdown_count
    User.save()
    return HttpResponse("User information updated successfully")