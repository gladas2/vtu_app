
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Transaction
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','password')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated):
        user = User.objects.create_user(**validated)
        return user

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('id','user','timestamp','success','provider_response')
