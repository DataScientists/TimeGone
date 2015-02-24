from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from core import views

urlpatterns = patterns(
    '',
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^projects/(\d+)/$', views.project, name='project'),
    url(r'^create/$', views.create, name='create'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^report/$', views.report, name='report'),
    url(r'^track/(\d+)/$', views.track, name='track'),
    url(r'^bigtime/', views.quick_track, name='quick_track'),
    url(r'^auth/register/$', views.register, name='register'),
    url(r'^auth/logout/$', auth_views.logout_then_login,
        name='logout'),
    url(r'^delete-tracked-time/(\d+)$', views.delete_tracked_time,
        name='delete-tracked-time'),
    # url(r'^tracked-time/(\d+)/(.+)$/', views.edit_tracked_time,
    #     name='edit-tracked-time')
    url(r'^time/delete/(\d+)$', views.time_delete, name="time_delete"),
    url(r'^time/project/(\d+)$', views.time_project_api, name="time_project_api"),
    url(r'^time/hours/(\d+)$', views.time_hours_api, name="time_hours_api"),
    url(r'^time/description/(\d+)$', views.time_description_api, name="time_description_api"),
    url(r'^time/track_date/(\d+)$', views.time_track_date_api, name="time_track_date_api")
)
