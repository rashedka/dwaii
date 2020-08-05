from .models import *
from rest_framework import serializers


class JsonUserInfo(serializers.ModelSerializer):
    class Meta:
        model = user_info
        fields = '__all__'
