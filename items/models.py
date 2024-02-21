from django.db import models
from users.models import User


# 项目
class Item(models.Model):
    # 项目名字
    name = models.CharField(max_length=32)
    # 项目的电量消耗
    electricityConsume = models.IntegerField()
    # 项目细节
    details = models.CharField(max_length=100)
    # 项目ddl
    ddl = models.CharField(max_length=32, null=True)
    # 项目绑定的用户
    itemUser = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # 项目的完成情况
    isCompleted = models.BooleanField(default=False)
