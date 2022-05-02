from django.urls import path, include
from rest_framework import routers
from rest_framework_extensions.routers import ExtendedDefaultRouter
from .views import PostViewSet, CommentViewSet
from .config import APP_NAME


router = ExtendedDefaultRouter()
(
    router.register(r'posts', PostViewSet, basename='post')
          .register(r'comments', CommentViewSet, basename='posts-comment',
                    parents_query_lookups=['post'])
)

app_name = APP_NAME
urlpatterns = [
    path('', include(router.urls)),
]
