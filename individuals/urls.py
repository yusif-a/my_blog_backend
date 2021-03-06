from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, GroupViewSet, PermissionViewSet
from .config import APP_NAME


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'permissions', PermissionViewSet, basename='permission')

app_name = APP_NAME
urlpatterns = [
    path('', include(router.urls)),
]
