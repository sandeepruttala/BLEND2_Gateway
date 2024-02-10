from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_, name='login'),
    path('register', views.register_, name='register'),
    path('home', views.home, name='home'),
    path('upload', views.upload, name='upload'),
]