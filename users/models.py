from django.db import models


# 用户表
class User(models.Model):
    name = models.CharField(max_length=32)
    password = models.IntegerField()
    electricity = models.IntegerField(default=100)
    # 与items有一个one to many关系
    completedItems = models.IntegerField(default=0)
    shutDownCount = models.IntegerField(default=0)
    token = models.CharField(max_length=1024, null=True, blank=True)
    session_key = models.CharField(max_length=1024, null=True, blank=True)
    openid = models.CharField(max_length=1024, null=True, blank=True)
