from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_extensions.mixins import NestedViewSetMixin
from .models import Post, Comment, Tag, PostViews, PostVotes, CommentVotes
from .serializers import PostSerializer, CommentAuthenticatedSerializer, CommentAnonymousSerializer, \
    TagSerializer, TagModelSerializer, PostVotesSerializer, CommentVotesSerializer
from .mixins import VoteViewSetMixin
from commons.permissions import IsSuperuserCreatorOrReadOnly, IsCreatorOrReadOnly

import logging
logger = logging.getLogger(__name__)


class PostViewSet(NestedViewSetMixin, VoteViewSetMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsSuperuserCreatorOrReadOnly]

    vote_model = PostVotes
    vote_model_foreign_key_field_name = 'post'
    vote_serializer_class = PostVotesSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def set_tags(self, request, pk=None):
        """
        Accepts a list of tags.
        Sets all tags of a Post object.
        Removing implicitly tags not included.
        """
        existing_tags = []
        new_tags_data = []
        new_tags_names = set()
        for tag_data in request.data:
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
            post.tags.clear()
            for tag in existing_tags:
                post.tags.add(tag)

            for tag_data in new_tags_data:
                tag_data.update({'creator': request.user})
                Tag.objects.create(**tag_data)

            return Response({'status': 'tags set'})
        else:
            return Response(tags_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        self.filter_tags(request)
        return super().list(request, *args, **kwargs)

    def filter_tags(self, request):
        """
        Filters a '+' delimited list of tags, assigned to a query_param named 'tags'.
        """
        if 'tags' in request.query_params:
            tag_names = request.query_params['tags'].split()
            for tag_name in tag_names:
                self.queryset = self.queryset.filter(tags__name=tag_name)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.set_post_view(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def set_post_view(self, request, post_instance):
        if request.user and request.user.is_authenticated:
            if PostViews.objects.filter(post=post_instance, creator=request.user).count() == 0:
                PostViews.objects.create(post=post_instance, creator=request.user)
        else:
            ip_address = self.get_client_ip(request)
            if PostViews.objects.filter(post=post_instance, ip_address=ip_address).count() == 0:
                PostViews.objects.create(post=post_instance, ip_address=ip_address)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class CommentViewSet(NestedViewSetMixin, VoteViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsCreatorOrReadOnly]

    vote_model = CommentVotes
    vote_model_foreign_key_field_name = 'comment'
    vote_serializer_class = CommentVotesSerializer

    def get_serializer_class(self):
        if self.request.user and self.request.user.is_authenticated:
            return CommentAuthenticatedSerializer
        return CommentAnonymousSerializer

    def perform_create(self, serializer):
        post_id = self.kwargs.get('parent_lookup_post')
        creator_data = dict()
        if self.request.user and self.request.user.is_authenticated:
            creator_data.update({'creator': self.request.user})
        serializer.save(post_id=post_id, **creator_data)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
