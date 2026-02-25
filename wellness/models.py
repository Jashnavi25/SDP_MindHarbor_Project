from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('student', 'Student'),
    ('counselor', 'Counselor'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class WellnessResource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(max_length=500)

class CounselingSession(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    counselor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='counseling_sessions')
    scheduled_time = models.DateTimeField()   # must be DateTimeField
    notes = models.TextField(blank=True, null=True)

class AnonymousSupport(models.Model):
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

