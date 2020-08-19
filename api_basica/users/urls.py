from django.urls import path

from users import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateuserView.as_view(), name='create'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]