from django.urls import (
    path,
    include
)
from apps.recipe import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'web-extension', views.WebExtensionAPI, basename='get_recipe_information'),
router.register(r'recipe-category', views.RecipeCategoryAPI, basename='save_recipe_category'),

urlpatterns = [
    path('', include(router.urls)),
]


