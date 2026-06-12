from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    avatar = serializers.FileField()
    email = serializers.EmailField()
    password = serializers.CharField()
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    
class UserIdSerializer(serializers.Serializer):
    userId = serializers.CharField()