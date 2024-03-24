from django.urls import (
    path,
    include
)
from apps.recipe import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'get-recipe-information', views.RecipeInformation, basename='get_recipe_information')

urlpatterns = [
    path('web-extension/', include(router.urls)),
    path('web-extension/recipe/', views.SaveRecipe.as_view(), name='save_recipe'),
]


