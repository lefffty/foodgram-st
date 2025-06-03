from rest_framework.routers import DefaultRouter
from django.urls import (
    include,
    path,
)

from . import views


router = DefaultRouter()

router.register(r'recipes', views.RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        's/<int:id>/',
        views.redirect_from_short_link,
        name='redirect_from_short_link'
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        views.add_shopping_cart,
    ),
    path(
        'recipes/<int:id>/favorite/',
        views.add_favourite_recipe,
    ),
    path(
        'recipes/download_shopping_cart/',
        views.shopping_cart_list,
    ),
    path('', include(router.urls)),
]
