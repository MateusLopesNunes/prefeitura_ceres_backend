from django.db import models
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Request, RequestType, Status, StatusCode, Commentary

class RequestSerializer(ModelSerializer):
    class Meta:
        model = Request
        #fields = '__all__'
        exclude = ['is_canceled', 'current_status']
        depth = 5

class RequestResposeSerializer(ModelSerializer):
    class Meta:
        model = Request
        exclude = ['is_canceled', ]
        depth = 5

class RequestTypeSerializer(ModelSerializer):
    class Meta:
        model = RequestType
        fields = '__all__'
        depth = 5

class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'
        depth = 5

class StatusCodeSerializer(ModelSerializer):
    class Meta:
        model = StatusCode
        fields = '__all__'
        depth = 5

class CommentarySerializer(ModelSerializer):
    class Meta:
        model = Commentary
        fields = '__all__'
        depth = 5