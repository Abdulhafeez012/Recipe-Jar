from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/v1/users/', include('apps.user_auth.urls')),
    path('api/v1/recipes/', include('apps.recipe.urls')),
    path('api/v1/shopping-list/', include('apps.shopping_list.urls')),
    path('api/v1/home-view/', include('apps.main.urls')),
]