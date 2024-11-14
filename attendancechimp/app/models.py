from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class People(models.Model):
    is_instructor = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, blank=True, null=True)
    instructor_id = models.CharField(max_length=20, blank=True, null=True)
    
class Course(models.Model):
    course_ID = models.CharField(max_length=30, primary_key=True)
    instructor = models.ForeignKey(People, on_delete=models.CASCADE,
                                   limit_choices_to={'is_instructor': True})
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    days = models.JSONField(default=list)

class Lecture(models.Model):
    lecture_time = models.DateTimeField()
    course_ID = models.ForeignKey(Course, on_delete=models.CASCADE)

class QR_Codes(models.Model):
    qr_code= models.FileField(upload_to="uploads/")
    uploader = models.OneToOneField(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    time_uploaded = models.DateTimeField()
    
