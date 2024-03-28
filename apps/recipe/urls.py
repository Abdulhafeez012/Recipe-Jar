from django.urls import (
    path,
    include
)
from apps.recipe import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'web-extension', views.WebExtensionAPI, basename='recipe_information'),
router.register(r'recipe-category', views.RecipeCategoryAPI, basename='recipe_category'),
router.register(r'', views.RecipeAPI, basename='recipe'),

urlpatterns = [
    path('', include(router.urls)),
]


