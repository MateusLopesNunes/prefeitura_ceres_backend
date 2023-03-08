from django.db import models
from user.models import Usuario

# Create your models here.

class RequestType(models.Model):
    icon= models.ImageField(upload_to = 'assets')
    banner = models.ImageField(upload_to = 'assets')
    desc= models.CharField(max_length=100)

    def __str__(self):
        return self.desc[0:50]

    class Meta:
        ordering = ['id']


class StatusCode(models.Model):
    desc = models.CharField(max_length=50)
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.desc[0:50]

    class Meta:
        ordering = ['id']


class Request(models.Model):
    id_user = models.ForeignKey(Usuario,on_delete=models.CASCADE, null=False)
    request_type = models.ForeignKey(RequestType, on_delete=models.CASCADE, null=False)
    importance = models.IntegerField(null=True)
    img1 = models.ImageField(upload_to = 'images')
    img2= models.ImageField(upload_to = 'images')
    img3= models.ImageField(upload_to = 'images')
    comment= models.TextField()
    lat= models.CharField(max_length=50)
    lon= models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True)
    is_canceled = models.BooleanField(default=False)
    current_status = models.ForeignKey(StatusCode,on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.comment[0:50]

    class Meta:
        ordering = ['-created']


class Status(models.Model):
    id_request = models.ForeignKey(Request,on_delete=models.CASCADE, null=False)
    status_code = models.ForeignKey(StatusCode,on_delete=models.CASCADE, null=False)
    dateTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-dateTime']
    