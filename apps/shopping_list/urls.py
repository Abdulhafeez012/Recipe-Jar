from django.urls import (
    path,
    include
)
from apps.shopping_list import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'category', views.ShoppingListCategoryAPI, basename='shopping_list_category')
router.register(r'', views.ShoppingListAPI, basename='shopping_list')

urlpatterns = [
    path('', include(router.urls)),
]
