from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class People(models.Model):
    person_type = models.BinaryField() 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Course(models.Model):
    course_ID = models.CharField(max_length=30)
    instructor = models.ForeignKey(People, on_delete=models.CASCADE)

class Enrollment(models.Model):
    course_ID = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(People, on_delete=models.CASCADE)

class Lecture(models.Model):
    lecture = models.DateTimeField()
    course_ID = models.ForeignKey(Course, on_delete=models.CASCADE)
    qr_code_string = models.CharField(max_length=30)

class QR_Codes(models.Model):
    upload = models.FileField(upload_to="uploads/")
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    time_uploaded = models.DateTimeField()
    
