from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Project(models.Model):
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()


class TrackedTime(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    created_at = models.DateTimeField(auto_now_add=True)
    hours = models.FloatField(validators=[MinValueValidator(0)])
    activity = models.CharField(max_length=255, default='')
    
