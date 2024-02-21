from rest_framework import serializers

from items.models import Item


# 项目的模型序列化器
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
