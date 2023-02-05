from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.

class UserType(models.Model):
    desc = models.CharField(max_length=100)

class Usuario(AbstractUser):
    username = None
    nome = models.CharField(max_length=255)
    dataNasc = models.DateField()
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=11)
    email = models.EmailField(max_length=255, unique=True, error_messages={'unique': "O email cadastrado já existe."})
    password = models.CharField(max_length=20)
    userType = models.ForeignKey(UserType,on_delete=models.CASCADE, null=False)
    
    USERNAME_FIELD = 'cpf'
    
    ordering = ('id',)
    def __str__(self):
        return self.nome[0:50]
        
    class Meta:
        ordering = ['id']
