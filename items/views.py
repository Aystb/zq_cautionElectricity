from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet

from items.models import Item
from django.shortcuts import render

from items.serializers import ItemSerializer


# Create your views here.
def index(request):
    return HttpResponse("items!")

# 创建项目
def createItem(request, userid):
    itemName = request.POST['itemName'],
    itemDetails = request.POST['details'],
    itemEleConsume = request.POST['electricityConsume'],
    itemDdl = request.POST['ddl']
    thisItemUser = userid
    Item.objects.create(name=itemName, ddl=itemDdl, details=itemDetails, electricityConsume=itemEleConsume[0],
                        itemUser_id=thisItemUser,complete=False)
    return HttpResponse("createItem")


# modelViewSet内部实现post、get、put、delete方法
# 该部分文档可本地运行项目后，访问http://127.0.0.1:8000/api/docs/，进行查看
class ItemViewSet(ModelViewSet):
    """
    create:
    上传项目
    delete: 删除项目
    update: 修改项目
    partial_update:这个没啥用，这个需要用patch方式做出http请求，作用是修改部分数据，实际上用put即可，实际开发中用的很少
    list: 获取所有项目，如需过滤请将过滤参数作为get的请求参数，目前是可以用所有字段进行过滤，后面待整体项目完善后会对字段进行限制
    retrieve: 获取单个项目
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    # 过滤条件要用get方法，参数会写在url上
    filter_fields = '__all__'
