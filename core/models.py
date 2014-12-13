from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from timezone_field import TimeZoneField


class Project(models.Model):
    COLOR_CHOICES = [(x, x) for x in ['#FF9500', '#FF3B30', 
                                  '#4CD964', '#FFCC00', '#BDBEC2', '#1F1F21',
                                  '#FF2D55', '#5856D6', '#007AFF', '#34AADC']]
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    color = models.CharField(null=True, choices=COLOR_CHOICES, max_length=7)

class TrackedTime(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    track_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hours = models.FloatField(validators=[MinValueValidator(0)])
    activity = models.CharField(max_length=255, default='')
    manual_date = models.BooleanField(default=False)


class Timezone(models.Model):
    user = models.ForeignKey(User)
    timezone = TimeZoneField(default='Europe/London')
