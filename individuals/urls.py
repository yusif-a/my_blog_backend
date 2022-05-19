from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet
from .config import APP_NAME


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

app_name = APP_NAME
urlpatterns = [
    path('', include(router.urls)),
]
