from django.db import models
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Request, RequestType, Status, StatusCode, Commentary

class RequestSerializer(ModelSerializer):
    class Meta:
        model = Request
        #fields = '__all__'
        exclude = ['is_canceled', 'current_status']

class RequestResposeSerializer(ModelSerializer):
    class Meta:
        model = Request
        exclude = ['is_canceled', ]

class RequestTypeSerializer(ModelSerializer):
    class Meta:
        model = RequestType
        fields = '__all__'

class StatusSerializer(ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class StatusCodeSerializer(ModelSerializer):
    class Meta:
        model = StatusCode
        fields = '__all__'

class CommentarySerializer(ModelSerializer):
    class Meta:
        model = Commentary
        fields = '__all__'