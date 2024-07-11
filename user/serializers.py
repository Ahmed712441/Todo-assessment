from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils import createAuth0User

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'name',
            'password'
        )
    
    def create(self, validated_data):
        email = validated_data.get('email')
        name = validated_data.get('name')
        password = validated_data.get('password')
        createAuth0User(email,password,name)
        return User.objects.create_user(email=email,name=name,password=password)