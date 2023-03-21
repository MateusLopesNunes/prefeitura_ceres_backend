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
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/requests/',
            'method': 'GET',
            'body': None,
            'description': ''
        },
        {
            'Endpoint': '/requests/<id>',
            'method': 'GET',
            'body': None,
            'description': ''
        },
        {
            'Endpoint': '/requests/create',
            'method': 'POST',
            'body': {'body': ""},
            'description': ''
        },
        {
            'Endpoint': '/requests/<id>/update',
            'method': 'PUT',
            'body': {'body': ""},
            'description': ''
        },
        {
            'Endpoint': '/requests/<id>/delete',
            'method': 'DELETE',
            'body': None,
            'description': ''
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_canceled', 'request_type', "current_status"]
    def getRequests(request):
        reqs = Request.objects.all()
        serializer = RequestResposeSerializer(reqs, many=True)
        return Response(serializer.data)
    

class GetRequestByType(generics.ListAPIView):
   #permission_classes = [IsAuthenticated] 
    serializer_class = RequestResposeSerializer
    def get_queryset(self):
        queryset = Request.objects.filter(request_type__pk=self.kwargs['pk'])
        return queryset
    
class GetRequestByStatusCode(generics.ListAPIView):
    #permission_classes = [IsAuthenticated] 
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
    serializer_class = RequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_canceled']
    def getRequest(request, pk):
        req = Request.objects.get(id=pk)
        serializer = RequestSerializer(req, many=False)
        return Response(serializer.data)

class GetRequestStatus(generics.ListAPIView):
    #permission_classes = [IsAuthenticated] 
    serializer_class = StatusSerializer
    def get_queryset(self):
        queryset = Status.objects.filter(id_request=self.kwargs['pk'])
        return queryset

class GetUserRequestStatus(generics.ListAPIView):
    #permission_classes = [IsAuthenticated] 
    serializer_class = StatusSerializer
    def get_queryset(self):
        queryset = Status.objects.filter(id_request_id__id_user = self.kwargs['pk'])
        return queryset

class GetStatus(generics.ListAPIView):
    #permission_classes = [IsAuthenticated] 
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_request']
    def getRequestStatus(request):
        req = Status.objects.all()
        serializer = StatusSerializer(req, many=True)
        return Response(serializer.data)

class GetStatusList(generics.ListAPIView):
    #permission_classes = [IsAuthenticated] 
    queryset = StatusCode.objects.all()
    serializer_class = StatusCodeSerializer

class GetUserRequests(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
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
    filter = Status.objects.filter(id_request=pk)
    status = filter[0]
    if status.status_code.desc == 'Em análise':
        status_code_req = StatusCode.objects.filter(pk=STATUS_CANCELED)
        newStatus = Status(id_request=status.id_request, status_code=status_code_req[0])
        newStatus.save()

        request = status.id_request
        request.is_canceled = True
        request.save()
        return Response({'message': "Requisição cancelada com sucesso"}, status=status_code.HTTP_200_OK)

    return Response({'message': "A requisição não está com o status inicial, portanto não pode ser cancelada"}, status=status_code.HTTP_400_BAD_REQUEST)


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

    status = Status(
        id_request= request_instance,
        status_code= status_code_instance
    )
    status.save()

    request_instance.current_status = status_code_instance
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
    #permission_classes = [IsAuthenticated]
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
    #permission_classes = [IsAuthenticated]
    queryset = RequestType.objects.all()
    serializer_class = RequestTypeSerializer

class deleteRequestType(generics.DestroyAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = RequestType.objects.all()
    serializer_class = RequestTypeSerializer
