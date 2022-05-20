from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin
from .models import User
from .config import APP_NAME


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['content_type_id', 'codename']


class GroupSerializer(PartialUpdateSerializerMixin,
                      serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'{APP_NAME}:group-detail')
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['url', 'name', 'permissions']


class UserSerializer(PartialUpdateSerializerMixin,
                     serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'{APP_NAME}:user-detail')
    groups = GroupSerializer(many=True, read_only=True)
    user_permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'is_superuser',
                  'is_staff', 'is_active', 'last_login', 'date_joined', 'groups', 'user_permissions']
