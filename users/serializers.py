from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import status

from utils.utils import CustomValidation
from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def save(self, **kwargs):
        # check if user with provided email already exists
        email = self.validated_data['email']

        if User.objects.filter(email=email).exists():
            raise CustomValidation(
                'User with provided email id already exists.', status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(**self.validated_data)
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')
