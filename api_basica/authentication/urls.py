from django.urls import path

from authentication import views

urlpatterns = [
    path('', views.CreateTokenView.as_view(), name='token'),
]