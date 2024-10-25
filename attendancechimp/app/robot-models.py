#prompt: a Django models.py for an attendance tracking system
#where a lecture generates a QR code, and students need to
#upload a picture of it for attendance confirmation.

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image  # Required for image processing

class Lecture(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    qr_code = models.ImageField(upload_to='qr_codes/')  # Field to store the QR code image

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d %H:%M')}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.user.username

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    uploaded_image = models.ImageField(upload_to='attendance_uploads/')  # Image upload field for QR code photo
    is_verified = models.BooleanField(default=False)  # Verified status of attendance

    def __str__(self):
        return f"Attendance for {self.student} in {self.lecture}"

    def save(self, *args, **kwargs):
        # Optional: Add logic here to verify uploaded image if needed.
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('student', 'lecture')  # Ensures unique attendance per lecture per student

