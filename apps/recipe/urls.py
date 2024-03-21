from django.urls import (
    path,
    include
)
from apps.recipe import views


urlpatterns = [
    path('web-extension/get-recipe-information/', views.RecipeInformation.as_view(), name='get_recipe_information'),
    path('web-extension/recipe/', views.SaveRecipe.as_view(), name='save_recipe'),
]

