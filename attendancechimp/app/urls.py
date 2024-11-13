from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_bio_view, name='team_bio'),
    path('app/new/', views.new_user_form, name='new_user_form'),
    path('app/new', views.new_user_form, name='new_user_form'),
    path('app/createUser', views.create_user, name='create_user'),
    path('app/createUser/', views.create_user, name='create_user'),
    path('app/new_course', views.new_course, name='course_create'), 
    path('app/new_lecture', views.new_lecture, name='qr_create'),
    path('app/new_qr_upload', views.new_qr_upload, name='qr_upload'),
    path('app/dumpUploads/', views.dumpUploads, name='dumpUploads'),
]

