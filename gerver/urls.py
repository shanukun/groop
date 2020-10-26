from django.urls import path, include
from .import views

urlpatterns = [
    path('register/', views.register_user, name='register-user'),
    path('create_group/', views.create_group, name='create-user'),
]
