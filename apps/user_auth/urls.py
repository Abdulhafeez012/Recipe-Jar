from apps.user_auth import views
from rest_framework import routers
from django.urls import (
    path,
    include
)

routers = routers.DefaultRouter()
routers.register(r'', views.RecipeUserAPI, basename='recipe_user')

urlpatterns = [
    path('', include(routers.urls)),
]




