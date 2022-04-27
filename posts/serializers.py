from rest_framework import serializers
from .models import Post
from .config import APP_NAME


class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'{APP_NAME}:post-detail')

    class Meta:
        model = Post
        fields = ['url', 'title', 'text', 'created_at', 'modified_at']