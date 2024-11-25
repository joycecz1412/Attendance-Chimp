from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class People(models.Model):
    is_instructor = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
class Course(models.Model):
    course_id = models.CharField(max_length=30, primary_key=True)
    instructor = models.ForeignKey(People, on_delete=models.CASCADE,
                                   limit_choices_to={'is_instructor': True})
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    days = models.JSONField(default=list)

class Lecture(models.Model):
    lecture_time = models.DateTimeField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    qrdata = models.CharField(max_length=16, null=True, blank=True)

class QR_Codes(models.Model):
    qr_code= models.FileField(upload_to="uploads/")
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE,null=True, blank=True)
    time_uploaded = models.DateTimeField()

def getUploadsForCourse(id):
    if not Course.objects.filter(course_id=id).exists():
        return []
    else:
        qr_codes = QR_Codes.objects.filter(course_id=id)
        return qr_codes
