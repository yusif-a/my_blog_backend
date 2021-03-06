from rest_framework import serializers
from rest_framework_extensions.serializers import PartialUpdateSerializerMixin
from commons.nested_hyperlinked_identity_field import NestedHyperlinkedIdentityField
from .models import Post, Comment, Tag, PostVotes, CommentVotes
from .config import APP_NAME
from individuals.serializers import UserSerializer
from individuals.models import User


class TagSerializer(PartialUpdateSerializerMixin,
                    serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'{APP_NAME}:tag-detail')
    creator = UserSerializer(read_only=True)

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
    my_vote = serializers.SerializerMethodField()

    def get_my_vote(self, obj):
        if not self._context['request'].user or not self._context['request'].user.is_authenticated:
            return None

        try:
            vote = PostVotes.objects.get(post=obj, creator=self._context['request'].user).vote
        except PostVotes.DoesNotExist:
            vote = 0
        return vote

    class Meta:
        model = Post
        fields = ['url', 'title', 'text', 'tags', 'creator', 'views_count', 'rating', 'my_vote', 'created_at', 'modified_at']
        read_only_fields = ['creator']


class CommentAuthenticatedSerializer(PartialUpdateSerializerMixin,
                                     serializers.HyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(view_name=f'{APP_NAME}:posts-comment-detail',
                                         lookup_url_kwargs=['parent_lookup_post', 'pk'],
                                         lookup_fields=['post_id', 'pk'])
    post = serializers.HyperlinkedRelatedField(view_name=f'{APP_NAME}:post-detail',
                                               read_only=True)
    creator = UserSerializer(read_only=True)
    mentioned_user = UserSerializer(read_only=True)
    mentioned_user_name = serializers.CharField(max_length=150, write_only=True,
                                                allow_blank=True, required=False)

    creator_name = serializers.CharField(read_only=True)

    my_vote = serializers.SerializerMethodField()

    def get_my_vote(self, obj):
        try:
            vote = CommentVotes.objects.get(comment=obj, creator=self._context['request'].user).vote
        except CommentVotes.DoesNotExist:
            vote = 0
        return vote

    def create(self, validated_data):
        # method 'create' is overridden instead of 'save', and 'update' is also not;
        # as 'mentioned_user' is not editable
        try:
            mentioned_user = User.objects.get(username=validated_data.pop('mentioned_user_name', None))
        except User.DoesNotExist:
            mentioned_user = None

        validated_data.update({'mentioned_user': mentioned_user})
        return super().create(validated_data)

    def validate_mentioned_user_name(self, value):
        try:
            if value:
                User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Mentioned user does not exist.")

        return value

    class Meta:
        model = Comment
        fields = ['url', 'post', 'text', 'creator', 'mentioned_user', 'creator_name',
                  'mentioned_user_name', 'rating', 'my_vote', 'created_at', 'modified_at']


class CommentAnonymousSerializer(CommentAuthenticatedSerializer):
    creator_name = serializers.CharField(max_length=100, allow_null=False, allow_blank=False)
    creator_email = serializers.EmailField(allow_null=False, allow_blank=False, write_only=True)

    # my_vote = None

    class Meta:
        model = Comment
        fields = ['url', 'post', 'text', 'creator', 'mentioned_user', 'creator_name', 'creator_email',
                  'mentioned_user_name', 'rating', 'created_at', 'modified_at']


class PostVotesSerializer(PartialUpdateSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PostVotes
        fields = ['vote']


class CommentVotesSerializer(PartialUpdateSerializerMixin, serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CommentVotes
        fields = ['vote']
