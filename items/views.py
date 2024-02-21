from django.http import HttpResponse
from items.models import Item
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse("items!")


def createItem(request, userid):
    itemName = request.POST['itemName'],
    itemDetails = request.POST['details'],
    itemEleConsume = request.POST['electricityConsume'],
    itemDdl = request.POST['ddl']
    thisItemUser = userid
    Item.objects.create(name=itemName, ddl=itemDdl, details=itemDetails, electricityConsume=itemEleConsume[0],
                        itemUser_id=thisItemUser,complete=False)
    return HttpResponse("createItem")
