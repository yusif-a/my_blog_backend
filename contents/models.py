from django.db import models
from individuals.models import User
from commons.abstract_models import CommonInfo


class Tag(CommonInfo, models.Model):
    name = models.SlugField(max_length=100, unique=True)


class Post(CommonInfo, models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='posts')


class Comment(CommonInfo, models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments',
                             editable=False)
    text = models.TextField()
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                       related_name='comments_mentioned_at',
                                       editable=False,
                                       null=True)
    # todo: rating







