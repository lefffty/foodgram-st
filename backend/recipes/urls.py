from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views


router = DefaultRouter()

router.register(r'recipes', views.RecipeViewSet, basename='recipes')

urlpatterns = [
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
