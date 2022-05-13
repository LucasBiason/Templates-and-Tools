from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 
from django.conf import settings
  
from src import views

urlpatterns = [
    path('', views.index_redirect, name='index'),
    path('admin/', admin.site.urls),
    path('auth/v1/token/', include('authentication.urls')),
    path('api/v1/users/', include('users.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)