from django.db import models
from individuals.models import User
from commons.abstract_models import CommonInfo


class Tag(CommonInfo, models.Model):
    name = models.SlugField(max_length=100, unique=True)


class PostViews(CommonInfo, models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)  # authenticated viewer
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # for anon user


class Post(CommonInfo, models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='posts')

    @property
    def views_count(self):
        return PostViews.objects.filter(post=self).count()


class Comment(CommonInfo, models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, editable=False, null=True)
    creator_name = models.CharField(max_length=100, null=True, blank=True)
    creator_email = models.EmailField(null=True, blank=True)  # confidential
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments',
                             editable=False)
    text = models.TextField()
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                       related_name='comments_mentioned_at',
                                       editable=False,
                                       null=True)
    # todo: rating







