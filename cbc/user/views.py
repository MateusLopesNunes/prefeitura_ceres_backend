from xml.dom import ValidationErr
from django.contrib.auth.models import User
from django.utils.encoding import force_str
from .models import Usuario, UserType
from .serializers import UsuarioSerializer, UsuarioPartialSerializer, UsuarioPassSerializer
from rest_framework.response import Response

from rest_framework import viewsets, generics

from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView

from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from random import choice
import string

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
User = get_user_model()

#Hateoas
@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/users/',
            'method': 'GET',
            'body': None,
            'description': 'Retorna am array de usuários'
        },
        {
            'Endpoint': '/users/<id>',
            'method': 'GET',
            'body': None,
            'description': 'Retorna um único objeto usuário'
        },
        {
            'Endpoint': '/users/create',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Cria novos usuários com dados enviados em pós-solicitação'
        },
        {
            'Endpoint': '/users/<id>/update',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Cria um usuário existente com os dados enviados'
        },
        {
            'Endpoint': '/users/`<id>/delete',
            'method': 'DELETE',
            'body': None,
            'description': 'Deleta um usuário existente'
        },
    ]
    return Response(routes)

#Utils
def generatePassword():
    size = 10
    values = string.ascii_letters + string.digits
    new_password = ''
    for i in range(size):
        new_password += choice(values)
    return new_password

def send_email(message, title, user_email):
    to_email = user_email
    email = EmailMessage(
                title, message, to=[to_email]
    )
    email.send()
    

#Andpoints
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Seu email foi confirmado')
    else:
        return HttpResponse('Link invalido!')

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ListaUsuarios(generics.ListAPIView):
    def get_queryset(self):
        queryset = Usuario.objects.all()
        return queryset
    serializer_class = UsuarioSerializer

class GetUsers(APIView): 
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        users = Usuario.objects.all()
        serializer = UsuarioSerializer(users, many=True)
        return Response(serializer.data)

class GetUser(APIView):       
    permission_classes = [IsAuthenticated]  
    def get(self, request, pk):
        user = Usuario.objects.get(pk=pk)
        serializer = UsuarioSerializer(user, many=False)
        return Response(serializer.data)

class GetLogin(APIView):       
    permission_classes = [IsAuthenticated]  
    def get(self, request, cpf):
        user = Usuario.objects.get(cpf=cpf)
        serializer = UsuarioSerializer(user, many=False)
        return Response(serializer.data)

@api_view(['POST'])
def createUser(request):
    CIDADAO = 1
    userType = UserType.objects.filter(id=CIDADAO)
    print(userType)

    user_email = User.objects.filter(email=request.data['email'])
    user_cpf = User.objects.filter(cpf=request.data['cpf'])

    if (user_email and user_cpf):
        return Response({"error": "Email e cpf informados já existem"}, status=status.HTTP_400_BAD_REQUEST)

    if (user_email):
        return Response({"error": "Este email já existe"}, status=status.HTTP_400_BAD_REQUEST)
    
    if (user_cpf):
        return Response({"error": "Este cpf já existe"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        data = request.data
        user = Usuario(
            nome = data['nome'],
            dataNasc = data['dataNasc'],
            cpf = data['cpf'],
            endereco = data['endereco'],
            telefone = data['telefone'],
            email = data['email'],
            is_active = False,
            userType = userType[0],
            #is_superuser = True,
            #is_staff = True
        )
        user.set_password(data['password'])
        user.save()

        current_site = get_current_site(request)
        mail_subject = 'Ative sua conta.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        send_email(message, mail_subject, user.email)

        return HttpResponse('Confirme seu email para confirmar o registro')

        #serializer = UsuarioSerializer(user, many=False)
       # return Response(serializer.data)

#@method_decorator(api_view(['PUT']), name='dispatch')
class UpdateUser(generics.UpdateAPIView):       
    permission_classes = [IsAuthenticated] 
    queryset = Usuario.objects.all()
    serializer_class = UsuarioPartialSerializer
    def updateUser(self, request, pk):
        data = request.data

        user = Usuario.objects.get(pk=pk)
        serializer = UsuarioPartialSerializer(user, data)
        if serializer.is_valid():
            serializer.update()

        return Response(serializer.data)


class UpdatePass(generics.UpdateAPIView):       
    permission_classes = [IsAuthenticated] 
    queryset = Usuario.objects.all()
    serializer_class = UsuarioPassSerializer
    def updatePass(self, request, pk):
        data = request.data

        user = Usuario.objects.get(pk=pk)
        user_arg = Usuario(user)
        #user.__setattr__('id',pk)
        
        user_arg.id = pk
        serializer = UsuarioPassSerializer(self, user_arg, data)
        if serializer.is_valid():
            serializer.update()

        return Response(serializer.data)


class DeleteUser(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated] 
    queryset = Usuario.objects.all()
    def deleteUser(request, pk):
        user = Usuario.objects.get(pk=pk)
        user.delete()
        return Response("Usuário Deletado")


@api_view(['POST'])
def resetPassword(request):
    email = request.data['email']
    cpf = request.data['cpf']

    userByEmail = User.objects.filter(email=email)
    userByCpf = User.objects.filter(cpf=cpf)
    
    if userByEmail and userByEmail[0].pk == userByCpf[0].pk:
        user = userByEmail[0]
        new_password = generatePassword()
        user.set_password(new_password)
        user.save()

        mail_subject = 'Recuperação de senha'
        message = f'Sua nova senha é: {new_password}'
        send_email(message, mail_subject, user.email)
        return Response({'message': 'A sua nova senha foi enviada para seu email'}, status=status.HTTP_200_OK)

    return Response({'error': 'Email ou cpf inválidos'}, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    

@api_view(['POST'])
def generate_jwt(request):
    cpf = request.data['cpf']
    password = request.data['password']

    is_activate = User.objects.filter(cpf=cpf)

    if (is_activate):
        if is_activate[0].is_active == False:
            return Response({'msg': 'A sua conta ainda não foi ativada'}, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(request, cpf=cpf, password=password)
    if user is not None:
        login(request, user)
        auth_data = get_tokens_for_user(request.user)
        return Response({'user_id': user.pk, **auth_data}, status=status.HTTP_200_OK)
    return Response({'msg': 'Credenciais inválidos'}, status=status.HTTP_401_UNAUTHORIZED)