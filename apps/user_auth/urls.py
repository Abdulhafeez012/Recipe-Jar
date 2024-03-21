from django.urls import (
    path,
    include
)
from apps.user_auth import views
from rest_framework import routers

# routers = routers.DefaultRouter()
# routers.register(r'list-users', views.ListUserView)

urlpatterns = [
    # path('', include(routers.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]




