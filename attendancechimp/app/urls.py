from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_bio_view, name='team_bio'),
    path('app/new/', views.new_user_form, name='new_user_form'),
    path('app/createUser/', views.create_user, name='create_user'),
]
