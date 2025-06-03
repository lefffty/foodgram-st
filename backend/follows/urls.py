from django.urls import path, include
from rest_framework import routers

from . import views


app_name = 'follows'

router = routers.DefaultRouter()
router.register(r'users', views.FollowViewSet, basename='follows')

urlpatterns = [
    path('', include(router.urls)),
]
