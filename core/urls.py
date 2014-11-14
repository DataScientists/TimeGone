from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from core import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^auth/register/$', views.register, name='register'),
    url(r'^auth/logout/$', auth_views.logout_then_login, name='logout')
)
