from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('recipe/manage/admin', admin.site.urls),
    path('api/v1/users/', include('apps.user_auth.urls')),
    path('api/v1/recipes/', include('apps.recipe.urls')),
    path('api/v1/shopping-list/', include('apps.shopping_list.urls')),
    path('api/v1/home-view/', include('apps.main.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
