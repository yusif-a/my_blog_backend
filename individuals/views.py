from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from commons.permissions import IsSuperuser
from .models import User
from .serializers import UserSerializer, GroupSerializer, PermissionSerializer
from commons.permissions import ReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperuser | ReadOnly]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsSuperuser]

    @action(detail=True, methods=['post'])
    def set_permissions(self, request, **kwargs):
        #  todo: input validation
        perms_q_object = Q(pk__in=[])  # always False Q object
        for perm_data in request.data:
            perms_q_object |= Q(content_type_id=perm_data['content_type_id'],
                                codename=perm_data['codename'])
        perms = Permission.objects.filter(perms_q_object)

        group = self.get_object()
        group.permissions.set(perms)

        return Response({'status': 'Permissions set'})

    @action(detail=True, methods=['post'])
    def add_user(self, request, **kwargs):
        #  todo: input validation
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        group = self.get_object()
        group.user_set.add(user)

        return Response({'status': 'User added'})

    @action(detail=True, methods=['post'])
    def remove_user(self, request, **kwargs):
        #  todo: input validation
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        group = self.get_object()
        group.user_set.remove(user)

        return Response({'status': 'User removed'})


class PermissionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsSuperuser]
