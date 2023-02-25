from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .serializers import RequestSerializer, RequestTypeSerializer, StatusSerializer,StatusCodeSerializer
from .models import Request, RequestType, Status, StatusCode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status as status_code
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

class GetRequests(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Request.objects.order_by('-created')
    serializer_class = RequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_canceled']
    def getRequests(request):
        reqs = Request.objects.all()
        serializer = RequestSerializer(reqs, many=True)
        return Response(serializer.data)

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
    serializer_class = RequestSerializer
    def get_queryset(self):
        queryset = Request.objects.filter(id_user=self.kwargs['pk'])
        return queryset

class CreateReq(generics.CreateAPIView):
    #permission_classes = [IsAuthenticated]
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    def createReq(request):
        data = request.data
        req = Request.objects.create(
            id_user = data['id_user'],
            request_type = data['request_type'],
            img1 = data['img1'],
            img2= data['img2'],
            img3= data['img3'],
            comment= data['comment'],
            lat= data['lat'],
            lon= data['lon'] 
        )
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
    
        
