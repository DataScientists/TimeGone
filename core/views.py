from __future__ import division
import logging
import time
from datetime import datetime


from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from forms import (
    RegisterForm, AddForm, LoginForm, TrackTimeForm,
    PasswordForm, TimezoneForm)
from models import Project, TrackedTime, Timezone
from django.db.utils import IntegrityError


@login_required
def settings(request):
    if request.method == 'POST':
        if 'password' == request.POST.get('action'):
            pf = PasswordForm(request.POST)
            tf = TimezoneForm()

            if pf.is_valid():
                ok = request.user.check_password(
                    pf.cleaned_data['old_password'])
                if ok:
                    request.user.set_password(
                        pf.cleaned_data['new_password'])
                    messages.success(request,
                                     'Password was changed.')
                    return redirect(request.path)
                else:
                    pf.add_error('old_password',
                                 'Wrong old password')
        elif 'tz' == request.POST.get('action'):
            pf = PasswordForm()
            obj, created = Timezone.objects.get_or_create(
                user=request.user)
            tf = TimezoneForm(request.POST, instance=obj)
            if tf.is_valid():
                tz = tf.save()
                messages.success(request,
                                 'Timezone set to {}'.format(
                                     tz.timezone))
                return redirect(request.path)
        else:
            pf = PasswordForm()
            tf = TimezoneForm()
    else:
        pf = PasswordForm()
        tf = TimezoneForm()
    return render(request, 'settings.html', {'password_form': pf,
                                             'tz_form': tf})


@login_required
def report(request, day, month, year):
    year = int(year)
    month = int(month)
    day = int(day)
    beginning = datetime(year, month, day, 0, 0, 0)
    ending = datetime(year, month, day, 23, 59, 59)
    qs = TrackedTime.objects.filter(user=request.user,
                                    created_at__gt=beginning,
                                    created_at__lt=ending).order_by('id')
    current_color = 0
    result = {}
    detailed = {}
    for x in qs:
        if x.project.id not in result:
            result[x.project.id] = {
                'color': current_color,
                'name': x.project.name,
                'hours': 0
            }
            current_color += 1
        result[x.project.id]['hours'] += x.hours
        detailed.setdefault(x.project.id, {'project': x.project,
                                           'timeset': []})
        detailed[x.project.id]['timeset'].append((x.hours, x.activity))
    detailed = [(v['project'], v['timeset']) for k, v in detailed.items()]
    color_classes = (
        ('progress-bar-primary', 'text-primary'),
        ('progress-bar-success', 'text-success'),
        ('progress-bar-info', 'text-info'),
        ('progress-bar-warning', 'text-warning'),
        ('progress-bar-danger', 'text-danger')
    )
    assert current_color <= len(color_classes), \
        "Too much projects to build progress bar"
    report = [{'id': k,
               'color_class': color_classes[v['color']][0],
               'legend_class': color_classes[v['color']][1],
               'name': v['name'], 'hours': v['hours'],
               'percent': v['hours'] / 24 * 100}
              for k, v
              in result.items()]
    report.sort(key=lambda x: x['name'])
    return render(request, 'report.html',
                  {'year': year, 'month': month, 'day': day,
                   'report': report,
                   'detailed': detailed})


@login_required
def track(request, _id):
    project = get_object_or_404(Project, id=_id, user=request.user)
    if request.method == 'POST':
        f = TrackTimeForm(request.POST)
        if f.is_valid():
            tr = f.save(commit=False)
            tr.project = project
            tr.user = request.user
            tr.save()
            return redirect('index')
    else:
        f = TrackTimeForm()
    return render(request, 'track.html', {'form': f, 'project': project})


@login_required
def index(request):
    qs = Project.objects.filter(user=request.user)
    report_date = time.strftime('%d/%m/%Y').split('/')
    report_date = {'day': report_date[0],
                   'month': report_date[1],
                   'year': report_date[2]}
    return render(request, 'index.html',
                  {'objects': qs, 'report_date': report_date})


@login_required
def add(request):
    if request.method == 'POST':
        f = AddForm(request.POST)
        if f.is_valid():
            p = f.save(commit=False)
            p.user = request.user
            p.save()
            return redirect('index')
    else:
        f = AddForm()
    return render(request, 'add.html', {'form': f})


@csrf_protect
def register(request):
    if request.method == 'POST':
        a = request.POST.get('action')
        if a == 'register':
            register_f = RegisterForm(request.POST)
            login_f = LoginForm()
            if register_f.is_valid():
                try:
                    User.objects.create_user(
                        register_f.cleaned_data['username'],
                        register_f.cleaned_data['email'],
                        register_f.cleaned_data['password'])
                except IntegrityError, e:
                    if 'username' in str(e):
                        register_f.add_error('username',
                                             'Username is taken')
                    elif 'email' in str(e):
                        register_f.add_error('email',
                                             'Email is already registered')
                    else:
                        raise e
                else:
                    user = authenticate(
                        username=register_f.cleaned_data['username'],
                        password=register_f.cleaned_data['password'])
                    login(request, user)
                    return redirect('index')
        elif a == 'login':
            register_f = RegisterForm()
            login_f = LoginForm(request.POST)
            if login_f.is_valid():
                user = authenticate(
                    username=login_f.cleaned_data['username'],
                    password=login_f.cleaned_data['password'])
                if user is None:
                    login_f.add_error('username',
                                      'Wrong credentials')
                else:
                    login(request, user)
                    return redirect('index')
        else:
            register_f = RegisterForm()
            login_f = LoginForm()
    else:
        register_f = RegisterForm()
        login_f = LoginForm()
    return render(request, 'register.html', {'register_form': register_f,
                                             'login_form': login_f})
