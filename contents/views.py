from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_extensions.mixins import NestedViewSetMixin
from .models import Post, Comment, Tag
from .serializers import PostSerializer, CommentSerializer, TagSerializer, TagModelSerializer
from commons.permissions import IsSuperuserCreatorOrReadOnly

import logging
logger = logging.getLogger(__name__)


class PostViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsSuperuserCreatorOrReadOnly]

    @action(detail=True, methods=['post'])
    def set_tags(self, request, pk=None):
        data = request.data
        existing_tags = []
        new_tags_data = []
        new_tags_names = set()
        for tag_data in data:
            try:
                tag_name = tag_data['name']
            except KeyError:
                pass  # will let serializer validation handle this
            else:
                try:
                    tag = Tag.objects.get(name=tag_name)
                except Tag.DoesNotExist:
                    if tag_name not in new_tags_names:
                        new_tags_names.add(tag_name)
                        new_tags_data.append(tag_data)
                else:
                    existing_tags.append(tag)

        tags_serializer = TagModelSerializer(data=new_tags_data, many=True)
        if tags_serializer.is_valid():
            post = self.get_object()
            for tag in existing_tags:
                post.tags.add(tag)

            for tag_data in new_tags_data:
                Tag.objects.create(creator=request.user, **tag_data)

            return Response({'status': 'tags set'})
        else:
            return Response(tags_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

