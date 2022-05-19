from django.db import models
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class VoteViewSetMixin:
    """
    Declare these three variables in viewset:
        vote_model
        vote_model_foreign_key_field_name
        vote_serializer_class
    """
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def vote(self, request, **kwargs):
        serializer = self.get_vote_serializer_class()(data=request.data)
        if serializer.is_valid():
            obj = self.get_object()
            obj_related_field_name = self.get_vote_model_foreign_key_field_name()
            vote_model = self.get_vote_model()
            try:
                instance = vote_model.objects.get(creator=request.user, **{obj_related_field_name: obj})
            except vote_model.DoesNotExist:
                serializer.save(creator=request.user, **{obj_related_field_name: obj})
            else:
                serializer.update(instance, serializer.validated_data)

            return Response({'status': 'vote received'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticatedOrReadOnly])
    def delete_vote(self, request, **kwargs):
        obj = self.get_object()
        obj_related_field_name = self.get_vote_model_foreign_key_field_name()
        votes_model = self.get_vote_model()
        votes_model.objects.filter(creator=request.user, **{obj_related_field_name: obj}).delete()
        return Response({'status': 'vote deleted'}, status=status.HTTP_204_NO_CONTENT)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_vote_serializer_class(self):
        assert hasattr(self, 'vote_serializer_class')
        return self.vote_serializer_class

    def get_vote_model_foreign_key_field_name(self) -> str:
        assert hasattr(self, 'vote_model_foreign_key_field_name')
        return self.vote_model_foreign_key_field_name

    def get_vote_model(self) -> models.Model:
        assert hasattr(self, 'vote_model')
        return self.vote_model
