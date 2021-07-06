from .serializers import *
from ecom.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework import generics, filters, status, mixins


class ProductView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    def get(self, request):
        query = Product.objects.all().filter(estado="Oferta")
        serializers = ProductSerializer(query, many=True, )
        return Response(serializers.data)

    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'price': request.data.get('price'),
            'name': request.data.get('name'),
            'id': request.data.get('id'),
        }
        serializer = ProductCrearSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductoCreateApi(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCrearSerializer



class ProductoUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCrearSerializer


class ProductoDeleteApi(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCrearSerializer


class CRUCAPIView(generics.ListCreateAPIView):
    search_fields = ['id']
    filter_backends = (filters.SearchFilter,)
    queryset = Product.objects.all()
    serializer_class = ProductCrearSerializer


class RegisterView(APIView):
    def post(self, request):
        serializers = Userserializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"error": False})
        return Response({"error": True})


class OrderView(APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        try:
            query = Orders.objects.all()
            serializers = OrdersSerializers(query, many=True)
            response_msg = {"error": False, "data": serializers.data}
        except:
            response_msg = {"error": True, "data": "no data"}
        return Response(response_msg)
