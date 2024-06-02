from rest_framework import serializers
from .models import UserToFriendMapping


class CreateRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserToFriendMapping
        fields = '__all__'


class UserFriendsSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='to_user.pk')
    email = serializers.EmailField(source='to_user.email')
    first_name = serializers.CharField(source='to_user.first_name')
    last_name = serializers.CharField(source='to_user.last_name')

    class Meta:
        model = UserToFriendMapping
        fields = ('user_id', 'email', 'first_name', 'last_name')
