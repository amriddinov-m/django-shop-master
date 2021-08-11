from django.contrib.auth.models import Group

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user.models import User, UserAddress


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'id', 'password', 'first_name', 'last_name', 'email', \
                 'username', 'is_active', 'user_type', 'phone',


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = Token
        fields = 'key', 'user', 'user_type'

    def get_user_type(self, obj):
        return obj.user.user_type


class UserAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAddress
        fields = '__all__'
