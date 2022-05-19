from django.urls import path, include
from rest_framework import routers
from rest_framework_extensions.routers import ExtendedDefaultRouter
from .views import PostViewSet, CommentViewSet, TagViewSet
from .config import APP_NAME


router = ExtendedDefaultRouter()
posts_router = router.register(r'posts', PostViewSet, basename='post')
comments_router = posts_router.register(r'comments', CommentViewSet, basename='posts-comment',
                                        parents_query_lookups=['post'])

tags_router = router.register(r'tags', TagViewSet)

app_name = APP_NAME
urlpatterns = [
    path('', include(router.urls)),
]
