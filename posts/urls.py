from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet
from .config import APP_NAME


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

app_name = APP_NAME
urlpatterns = [
    path('', include(router.urls)),
]
