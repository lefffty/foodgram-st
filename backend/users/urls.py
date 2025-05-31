from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'users'

router = DefaultRouter()

router.register(
    r'users',
    views.ProfileViewSet,
    basename='profile'
)

router.register(
    r'users',
    views.UserListCreateViewSet,
    basename='user_list_create'
)

router.register(
    r'users',
    views.UserDetailViewSet,
    basename='user_detail'
)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'users/set_password/',
        views.SetPasswordViewSet.as_view(
            {
                'post': 'set_password',
            }
        ),
    ),
    path(
        'users/me/avatar/',
        views.AvatarViewSet.as_view(
            {
                'put': 'set_avatar',
                'delete': 'delete_avatar',
            }
        )
    ),
    path('', include(router.urls)),
]
