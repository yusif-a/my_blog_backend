from django.urls import path, include
from rest_framework import routers
from rest_framework_extensions.routers import ExtendedDefaultRouter
from .views import PostViewSet, CommentViewSet, TagViewSet
from .config import APP_NAME


posts_router = ExtendedDefaultRouter()
(
    posts_router.register(r'posts', PostViewSet, basename='post')
          .register(r'comments', CommentViewSet, basename='posts-comment',
                    parents_query_lookups=['post'])
)

tags_router = routers.DefaultRouter()
tags_router.register(r'tags', TagViewSet)

app_name = APP_NAME
urlpatterns = [
    path('', include(posts_router.urls)),
    path('', include(tags_router.urls)),
]
