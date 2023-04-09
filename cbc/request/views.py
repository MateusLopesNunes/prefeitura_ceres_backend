import base64
from io import BytesIO
import uuid
from PIL import Image
from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import RequestSerializer, RequestTypeSerializer, RequestResposeSerializer, StatusSerializer,StatusCodeSerializer, CommentarySerializer
from .models import Request, RequestType, Status, StatusCode, Usuario, Commentary
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status as status_code
from django.core.files.base import ContentFile
from datetime import datetime, timedelta
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
def getRoutes(request):
    comment = {"id_request": "10", "id_user": "1", "message": "Café extra forte não é Café"}
    routes = [
        {
            'Endpoint': '/request/reqs?request_type=<id>&current_status=<id>&start_date=<2023-03-13>&end_date=<2023-03-17>',
            'method': 'GET',
            'body': None,
            'description': 'Busca todos os requests e aplica vários filtros simultaneamente'
        },
        {
            'Endpoint': '/request/comment/?request_id=<id>',
            'method': 'GET',
            'body': None,
            'description': 'Busca todos os comentários ou busca todos os comentários de um request'
        },
        {
            'Endpoint': f'/request/create/comment/',
            'method': 'POST',
            'body': comment,
            'description': 'Cadastra um comentário'
        },
    ]
    return Response(routes)

# Util
def base64_to_image(base64_string):
    #format, imgstr = base64_string.split(';base64,')
    #ext = format.split('/')[-1]
    return ContentFile(base64.b64decode(base64_string), name=uuid.uuid4().hex + ".jpg")

class GetRequests(generics.ListAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Request.objects.order_by('-created')
    serializer_class = RequestResposeSerializer
    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['is_canceled', 'request_type', "current_status"]
    #filterset_fields = ['is_canceled']
    #filterset_class = ProdutoFilter

    def get_queryset(self):
        queryset = Request.objects.all()

        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(current_status__icontains=search) | 
                Q(request_type__icontains=search) |
                Q(created__icontains=search) 
            )

        current_status = self.request.query_params.get('current_status', None)
        if current_status:
            queryset = queryset.filter(current_status=current_status)

        request_type = self.request.query_params.get('request_type', None)
        if request_type:
            queryset = queryset.filter(request_type=request_type)

        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date and end_date:
            date = datetime.strptime(start_date, '%Y-%m-%d').date()
            new_start_date = date + timedelta(-1)

            date = datetime.strptime(end_date, '%Y-%m-%d').date()
            new_end_date = date + timedelta(1)
            queryset = queryset.filter(created__range=[new_start_date, new_end_date])
    
        return queryset
    

class GetRequestByType(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = RequestResposeSerializer
    def get_queryset(self):
        queryset = Request.objects.filter(request_type__pk=self.kwargs['pk'])
        return queryset
    
class GetRequestByStatusCode(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = RequestResposeSerializer
    def get_queryset(self):
        queryset = Status.objects.filter(status_code__pk=self.kwargs['pk'])
        requests = []
        for status in queryset:
            requests.pop(status.id_request)
        return requests


class GetRequest(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated] 
    queryset = Request.objects.all()
    serializer_class = RequestResposeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_canceled']
    def getRequest(request, pk):
        req = Request.objects.get(id=pk)
        serializer = RequestResposeSerializer(req, many=False)
        return Response(serializer.data)

class GetRequestStatus(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = StatusSerializer
    def get_queryset(self):
        queryset = Status.objects.filter(id_request=self.kwargs['pk'])
        return queryset

class GetUserRequestStatus(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = StatusSerializer
    def get_queryset(self):
        queryset = Status.objects.filter(id_request_id__id_user = self.kwargs['pk'])
        return queryset


class GetStatus(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_request']
    def getRequestStatus(request):
        req = Status.objects.all()
        serializer = StatusSerializer(req, many=True)
        return Response(serializer.data)

class GetStatusList(generics.ListAPIView):
    permission_classes = [IsAuthenticated] 
    queryset = StatusCode.objects.all()
    serializer_class = StatusCodeSerializer

class GetUserRequests(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Request.objects.all()
    serializer_class = RequestResposeSerializer
    def get_queryset(self):
        queryset = Request.objects.filter(id_user=self.kwargs['pk'])
        return queryset


@api_view(['POST'])
def createReq(request):
    data = request.data

    user = Usuario.objects.filter(id=data['id_user'])
    request_type = RequestType.objects.filter(id=data['request_type'])
    req = Request.objects.create(
        id_user = user[0],
        request_type = request_type[0],
        img1 = base64_to_image(data['img1']),
        img2= base64_to_image(data['img2']),
        img3= base64_to_image(data['img3']),
        comment= data['comment'],
        lat= data['lat'],
        lon= data['lon'],
        current_status_updated_at= datetime.now()
    )
    req.save()

    EM_ANDAMENTO = 1
    status_code_req = StatusCode.objects.filter(id=EM_ANDAMENTO)
    status_req = Status(id_request=req, status_code=status_code_req[0])
    status_req.save()

    serializer = RequestSerializer(req, many=False)
    return Response(serializer.data)
    

class CreateStatus(generics.CreateAPIView):
    permission_classes = [IsAuthenticated] 
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    def createStatus(request, pk):
        data = request.data
        
        status = Status.objects.create(
            id_request = data['id'],
            status_code = 1
        )
        status_serializer = StatusSerializer(status, many=False)
        return status_serializer

class UpdateReq(generics.UpdateAPIView):       
    permission_classes = [IsAuthenticated]
    queryset = Request.objects.filter(is_canceled=False)
    serializer_class = RequestSerializer
    def updateReq(request, pk):
        data = request.data
        req = Request.objects.get(id=pk)
        serializer = RequestSerializer(req, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cancel_req(request, pk):
    STATUS_CANCELED = 5
    STATUS_EM_ADAMENTO = 1
    filter = Request.objects.filter(id=pk)

    if len(filter) == 0:
        return Response({'msg':'Esta solicitação não existe'})

    request = filter[0]
    if request.current_status.pk == STATUS_EM_ADAMENTO:
        status_code_req = StatusCode.objects.filter(pk=STATUS_CANCELED)

        if len(status_code_req) == 0:
            return Response({'msg':'Este código de status não existe'})

        newStatus = Status(id_request=request, status_code=status_code_req[0])
        newStatus.save()

        request.is_canceled = True
        request.current_status = status_code_req[0]
        request.current_status_updated_at = datetime.now()
        request.save()
        return Response({'msg': "Requisição cancelada com sucesso"}, status=status_code.HTTP_200_OK)

    return Response({'msg': "A requisição não está com o status inicial, portanto não pode ser cancelada"}, status=status_code.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def change_request(request, pk, status_code):
    requests_instance = Request.objects.filter(id=pk)
    status_codes_instance = StatusCode.objects.filter(id=status_code)

    if len(requests_instance) == 0:
        return Response({'msg':'Solicitação não existe'})
    
    if len(status_codes_instance) == 0:
        return Response({'msg':'Código do status não existe'})

    request_instance = requests_instance[0]
    status_code_instance = status_codes_instance[0]

    if status_code_instance.pk > 3:
        return Response({'msg':'Código do status inválido'})

    status = Status(
        id_request= request_instance,
        status_code= status_code_instance
    )
    status.save()

    request_instance.current_status = status_code_instance
    request_instance.current_status_updated_at = datetime.now()
    request_instance.save()
    return Response({'msg': 'Status da solicitção atualizada com sucesso'})


@api_view(['POST'])
def create_commentary(request):
    data = request.data
    id_request = Request.objects.filter(id=data['id_request'])
    id_user = Usuario.objects.filter(id=data['id_user'])

    if len(id_request) == 0:
        return Response({'msg':'Solicitação não existe'})
    
    if len(id_user) == 0:
        return Response({'msg':'Usuário não existe'})

    comment = Commentary(
        id_request= id_request[0],
        id_user= id_user[0],
        message= data['message']
    )

    comment.save()
    serializer = CommentarySerializer(comment)
    return Response(serializer.data)


class GetComments(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Commentary.objects.order_by('-created_at')
    serializer_class = CommentarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_request']

    def getComments(request):
        reqsT = Commentary.objects.all()
        serializer = CommentarySerializer(reqsT, many=True)
        return Response(serializer.data)


class DeleteReq(generics.DestroyAPIView):       
    permission_classes = [IsAuthenticated]
    queryset = Request.objects.filter(is_canceled=False)
    serializer_class = RequestSerializer 
    def deleteReq(request,pk):
        req = Request.objects.get(id=pk)
        req.delete()
        return Response("Req was deleted!")

class GetRequestsType(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = RequestType.objects.all()
    serializer_class = RequestTypeSerializer
    def getRequestsType(request):
        reqsT = RequestType.objects.all()
        serializer = RequestTypeSerializer(reqsT, many=True)
        return Response(serializer.data)
    
class createRequestType(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = RequestType.objects.all()
    serializer_class = RequestTypeSerializer

class deleteRequestType(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = RequestType.objects.all()
    serializer_class = RequestTypeSerializer
