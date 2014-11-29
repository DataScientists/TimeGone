from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from core import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^report/(\d{4})-(\d+)-(\d+)/$', views.report, name='report'),
    url(r'^track/(\d+)/$', views.track, name='track'),
    url(r'^auth/register/$', views.register, name='register'),
    url(r'^auth/logout/$', auth_views.logout_then_login, name='logout')
)
