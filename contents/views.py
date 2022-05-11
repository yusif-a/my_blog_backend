from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_extensions.mixins import NestedViewSetMixin
from .models import Post, Comment, Tag
from .serializers import PostSerializer, CommentSerializer, TagSerializer
from commons.permissions import IsSuperuserCreatorOrReadOnly

import logging
logger = logging.getLogger(__name__)


class PostViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsSuperuserCreatorOrReadOnly]

    def get_serializer_context(self):
        context = self.add_request_to_serializer_context(super().get_serializer_context())
        return context

    def add_request_to_serializer_context(self, context):
        context.update({'request': self.request})
        return context


class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs.get('parent_lookup_post')
        serializer.save(post_id=post_id)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = self.add_request_to_serializer_context(super().get_serializer_context())
        return context

    def add_request_to_serializer_context(self, context):
        context.update({'request': self.request})
        return context

