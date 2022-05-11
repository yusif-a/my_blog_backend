from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin
from .models import User


class UserSerializer(PartialUpdateSerializerMixin,
                     serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
