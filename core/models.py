from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from timezone_field import TimeZoneField

from constants import COLORS


class Project(models.Model):
    # from http://ios7colors.com
    COLOR_CHOICES = map(lambda x: (x, x), COLORS.keys())
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    color = models.CharField(null=True, choices=COLOR_CHOICES, max_length=18)

    def __unicode__(self):
        return self.name


class TrackedTime(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    track_date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hours = models.FloatField(validators=[MinValueValidator(0)])
    satisfaction = models.IntegerField(default=0)
    tags = models.CharField(max_length=255,default='')
    description = models.CharField(max_length=255, default='')
    manual_date = models.BooleanField(default=False)


class Timezone(models.Model):
    user = models.ForeignKey(User)
    timezone = TimeZoneField(default='Europe/London')
