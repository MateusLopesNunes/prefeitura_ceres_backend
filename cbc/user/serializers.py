from .models import Usuario, UserType
from rest_framework import serializers

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

class UsuarioSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label="Senha"
    )

    password_confirm = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label="Confirme a senha"
    )

    is_staff = serializers.BooleanField(
        label="Membro da Equipe",
        help_text="Indica que usuário consegue acessar o site de administração."
    )

    is_superuser = serializers.BooleanField(
        label="SuperUsuário",
        help_text="Indica que este usuário tem todas as permissões sem atribuí-las explicitamente."
    )

    class Meta:
        model = Usuario
        fields = ('id','nome','email','cpf','endereco','telefone','dataNasc', 'password', 'password_confirm', 'is_staff', 'is_superuser')
        extra_kwargs = {'password': {'write_only': True},'id': {'read_only': True}}

    def save(self):
        conta = Usuario(
            email=self.validated_data['email'], 
            nome=self.validated_data['nome'],
            is_staff=self.validated_data['is_staff'],
            is_superuser=self.validated_data['is_superuser'],
            dataNasc=self.validated_data['dataNasc'],  
            cpf=self.validated_data['cpf'], 
            endereco=self.validated_data['endereco'], 
            telefone=self.validated_data['telefone'], 
            is_active = False,
        )
        password = self.validated_data['password']
        password_confirm = self.validated_data['password_confirm']
    
        if password != password_confirm:
            raise serializers.ValidationError({'password': 'As senhas não são iguais.'})
        conta.set_password(password)
        conta.save()

        current_site = get_current_site(self)
        mail_subject = 'Ative sua conta.'
        message = render_to_string('acc_active_email.html', {
            'user': conta,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(conta.pk)),
            'token':account_activation_token.make_token(conta),
        })
        to_email = conta.email
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()

        return HttpResponse('Confirme seu email para confirmar o registro')

    def update(self):
        conta = Usuario(
            email=self.validated_data['email'], 
            nome=self.validated_data['nome'],
            dataNasc=self.validated_data['dataNasc'],  
            cpf=self.validated_data['cpf'], 
            endereco=self.validated_data['endereco'], 
            telefone=self.validated_data['telefone'], 
        ) 
        conta.save()
        return conta

class UsuarioPassSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(
        label="Id"
    )

    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label="Senha Atual"
    )

    new_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label="Nova senha"
    )

    new_password_confirm = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        label="Confirme a nova senha"
    )

    class Meta:
        model = Usuario
        fields = ('id','password','new_password','new_password_confirm') 

    def update(self, user, data):
        
        new_user = Usuario(
            email=user.email, 
            nome=user.nome,
            dataNasc=user.dataNasc,  
            cpf=user.cpf, 
            endereco=user.endereco, 
            telefone=user.telefone, 
            userType=user.userType 
        ) 

        password2 = data['new_password']
        new_user.id = data['id']
        new_user.set_password(password2)
    
        new_user.save()
        return new_user

class UsuarioPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('nome','email','cpf','endereco','telefone','dataNasc')
        
    def update(self, user, data):
        user.__setattr__('email',data['email'])
        user.__setattr__('nome',data['nome'])
        user.__setattr__('dataNasc',data['dataNasc'])  
        user.__setattr__('cpf',data['cpf'])
        user.__setattr__('endereco',data['endereco']) 
        user.__setattr__('telefone', data['telefone'])
    
        user.save()
        return user