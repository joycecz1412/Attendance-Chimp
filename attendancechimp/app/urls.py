from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.team_bio_view, name='team_bio'),
    path('app/new/', views.new_user_form, name='new_user_form'),
    path('app/new', views.new_user_form, name='new_user_form'),
    path('app/createUser', views.create_user, name='create_user'),
    path('app/createUser/', views.create_user, name='create_user'),
    path('app/new_course', views.new_course, name='new_course'),
    path('app/createCourse/', views.create_course, name='create_course'),
    path('app/createLecture/', views.create_lecture, name='create_lecture'),
    path('app/new_qr_upload', views.new_qr_upload, name='new_qr_upload'),
    path('app/createQRCodeUpload/', views.new_qr_upload, name='create_qr_upload'),
    path('app/dumpUploads/', views.dumpUploads, name='dumpUploads'),
]

