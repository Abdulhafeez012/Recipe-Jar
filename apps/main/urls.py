from django.urls import (
    path,
    include
)
from apps.main import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', views.HomeViewAPI, basename='home_view')

urlpatterns = [
    path('', include(router.urls)),
]
