from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from timezone_field import TimeZoneField


class Project(models.Model):
    # from http://ios7colors.com
    COLOR_CHOICES = map(lambda x: (x, x),
                        ['rgb(251, 0, 7)', 'rgb(240, 192, 193)',
                         'rgb(163, 75, 10)', 'rgb(200, 176, 42)',
                         'rgb(32, 246, 6)', 'rgb(24, 147, 11)',
                         'rgb(36, 174, 255)', 'rgb(20, 158, 156)',
                         'rgb(0, 0, 255)', 'rgb(240, 253, 57)',
                         'rgb(144, 196, 35)', 'rgb(217, 0, 204)',
                         'rgb(97, 0, 129)', 'rgb(200, 0, 93)',
                         'rgb(212, 100, 240)', 'rgb(253, 134, 9)',
                         'rgb(236, 40, 9)', 'rgb(253, 197, 11)',
                         'rgb(239, 210, 118)', 'rgb(238, 154, 40)',
                         'rgb(95, 254, 238)', 'rgb(194, 204, 223)',
                         'rgb(89, 100, 104)', 'rgb(0, 0, 0)'])
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
    activity = models.CharField(max_length=255, default='')
    manual_date = models.BooleanField(default=False)


class Timezone(models.Model):
    user = models.ForeignKey(User)
    timezone = TimeZoneField(default='Europe/London')
