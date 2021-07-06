from rest_framework import serializers
from ecom.models import *
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id','product_image','marca', 'price','description','name','categoria')
        depth = 1

class ProductCrearSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"
        depth = 1

class ImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"



class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password',
                  'first_name', 'last_name', 'email',)
        extra_kwargs = {'password': {"write_only": True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user



class OrdersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"
        depth = 1

