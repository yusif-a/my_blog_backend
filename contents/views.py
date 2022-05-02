from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

import logging
logger = logging.getLogger(__name__)


class PostViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs.get('parent_lookup_post')
        serializer.save(post_id=post_id)
