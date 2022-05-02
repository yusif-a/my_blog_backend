from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin
from commons.nested_hyperlinked_identity_field import NestedHyperlinkedIdentityField
from .models import Post, Comment
from .config import APP_NAME


class PostSerializer(PartialUpdateSerializerMixin,
                     serializers.HyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(view_name=f'{APP_NAME}:post-detail')

    class Meta:
        model = Post
        fields = ['url', 'title', 'text', 'created_at', 'modified_at']


class CommentSerializer(PartialUpdateSerializerMixin,
                        serializers.HyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(view_name=f'{APP_NAME}:posts-comment-detail',
                                         lookup_url_kwargs=['parent_lookup_post', 'pk'],
                                         lookup_fields=['post_id', 'pk'])
    post = serializers.HyperlinkedRelatedField(view_name=f'{APP_NAME}:post-detail',
                                               read_only=True)

    class Meta:
        model = Comment
        fields = ['url', 'post', 'text', 'created_at', 'modified_at']
