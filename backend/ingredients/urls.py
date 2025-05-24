from rest_framework.routers import DefaultRouter
from django.urls import include, path

from . import views


router = DefaultRouter()

router.register(
    r'ingredients',
    views.IngredientListViewSet,
    basename='ingredients'
)


urlpatterns = [
    path('', include(router.urls)),
]
