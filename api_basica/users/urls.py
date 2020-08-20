from django.urls import path
from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
router.register('users', views.ManageUserView)

app_name = 'user'

urlpatterns = [
]  + router.urls