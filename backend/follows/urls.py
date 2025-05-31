from django.urls import path

from . import views


app_name = 'follows'


urlpatterns = [
    path(
        'users/<int:pk>/subscribe/',
        views.FollowViewSet.as_view(
            {
                'post': 'subscribe',
                'delete': 'unsubscribe',
            }
        ),
        name='user_follow_unfollow',
    ),
    path(
        'users/subscriptions/',
        views.FollowViewSet.as_view(
            {
                'get': 'list_subscriptions',
            }
        )
    ),
]
