from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # pages
    path('login', views.login_, name='login'),
    path('logout', views.logout_, name='logout'),
    path('register', views.register_, name='register'),
    path('home', views.home, name='home'),

    # apis
    path('upload', views.upload, name='upload'),
]