from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin
from .models import User
from .config import APP_NAME


class UserSerializer(PartialUpdateSerializerMixin,
                     serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'{APP_NAME}:user-detail')

    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'is_superuser',
                  'is_staff', 'is_active', 'last_login', 'date_joined']
