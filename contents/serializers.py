from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin
from commons.nested_hyperlinked_identity_field import NestedHyperlinkedIdentityField
from .models import Post, Comment, Tag
from .config import APP_NAME
from individuals.serializers import UserSerializer


class TagSerializer(PartialUpdateSerializerMixin,
                    serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'{APP_NAME}:tag-detail')
    creator = UserSerializer(read_only=True)

    def create(self, validated_data):
        validated_data.update({'creator': self._context['request'].user})
        return super().create(validated_data)

    class Meta:
        model = Tag
        fields = ['url', 'name', 'creator', 'created_at', 'modified_at']
        read_only_fields = ['creator']


class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(PartialUpdateSerializerMixin,
                     serializers.HyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(view_name=f'{APP_NAME}:post-detail')
    creator = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['url', 'title', 'text', 'tags', 'creator', 'created_at', 'modified_at']
        read_only_fields = ['creator']


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
