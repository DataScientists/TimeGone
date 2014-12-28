from __future__ import division

import json
import logging

from datetime import date, timedelta

import arrow

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Sum
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import formats
from django.views.decorators.csrf import csrf_protect

from constants import abbr2color
from forms import (
    RegisterForm, CreateProjectForm, LoginForm, TrackTimeForm,
    PasswordForm, TimezoneForm, QuickTrackForm)
from models import Project, TrackedTime, Timezone


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
def report(request):
    if 'd' in request.GET:
        year, month, day = map(int, request.GET['d'].split('-'))
        x_day = date(year, month, day)
    else:
        a = get_user_date(request.user)
        year = a.year
        month = a.month
        day = a.day
        x_day = a.date()

    qs = TrackedTime.objects.filter(
        user=request.user,
        track_date=x_day).order_by('id')

    current_color = 0
    result = {}
    detailed = {}
    total_hours = 0
    for x in qs:
        if x.project.id not in result:
            result[x.project.id] = {
                'color': current_color,
                'name': x.project.name,
                'hours': 0
            }
            current_color += 1
        result[x.project.id]['hours'] += x.hours
        total_hours += x.hours
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
               'percent': v['hours'] / total_hours * 100}
              for k, v
              in result.items()]
    report.sort(key=lambda x: x['name'])
    return render(request, 'report.html',
                  {'year': year, 'month': month, 'day': day,
                   'report': report,
                   'detailed': detailed})


def get_user_date(user, d=None):
    if user.timezone_set.exists():
        tz = user.timezone_set.all()[0].timezone
        try:
            if d is None:
                a = arrow.now(tz)
            else:
                a = arrow.Arrow.strptime(d, '%Y-%m-%d', tz)
        except arrow.parser.ParserError:
            logging.exception('invalid tz %s for user %s', tz, user.id)
            if d is None:
                a = arrow.utcnow()
            else:
                a = arrow.Arrow.strptime(d, '%Y-%m-%d')
    else:
        logging.error('missing tz for user %s', user.id)
        if d is None:
            a = arrow.utcnow()
        else:
            a = arrow.Arrow.strptime(d, '%Y-%m-%d')
    return a


@login_required
def track(request, _id):
    project = get_object_or_404(Project, id=_id, user=request.user)
    if request.method == 'POST':
        f = TrackTimeForm(request.POST)
        if f.is_valid():
            obj = f.save(commit=False)
            obj.project = project
            obj.user = request.user
            if f.cleaned_data['track_date'] is None:
                obj.manual_date = False
                a = get_user_date(request.user)
                obj.track_date = a.date()
            else:
                obj.manual_date = True
            obj.save()
            messages.success(
                request,
                'Added {} hours for {} at date {}'.format(
                    obj.hours, obj.activity, fdate(obj.track_date)))
            return redirect('projects')
    else:
        f = TrackTimeForm()
    return render(request, 'track.html', {'form': f, 'project': project})


def get_graph(user, date):
    return json.dumps({
        'g': list(TrackedTime.objects
                  .filter(user=user, track_date=date)
                  .values('project', 'project__name', 'project__color')
                  .annotate(hours=Sum('hours'))
                  .order_by('project__name'))})


def fdate(x):
    return formats.date_format(x, 'SHORT_DATE_FORMAT')


@login_required
def dashboard(request):
    if request.is_ajax():
        selected = get_user_date(request.user, str(request.GET['date']))
        response = HttpResponse(get_graph(request.user, selected.date()))
        response['Content-Type'] = 'application/json'
        return response

    today = get_user_date(request.user).date()
    if 'date' in request.GET:
        selected = get_user_date(request.user, str(request.GET['date'])).date()
    else:
        selected = today
    qs = TrackedTime.objects.filter(user=request.user)\
                            .distinct()\
                            .values('track_date')\
                            .order_by('-track_date')
    dates = [x['track_date'] for x in qs]
    if len(dates) == 0 or today != dates[0]:
        dates.insert(0, today)
    yesterday = today - timedelta(days=1)
    if dates[1] != yesterday:
        dates.insert(1, yesterday)
    dates = map(fdate, dates)
    graph = get_graph(request.user, selected)
    return render(request, 'dashboard.html',
                  {'graph': graph, 'dates': dates,
                   'selected_date': fdate(selected),
                   'today_date': fdate(today),
                   'yesterday_date': fdate(yesterday)})


@login_required
@csrf_exempt
def project(request, project_id):
    p = get_object_or_404(Project, user=request.user, id=project_id)
    if request.method == 'POST':
        a = request.POST['attr']
        if a in ['name', 'description']:
            setattr(p, a, request.POST['text'])
            p.save()
            return HttpResponse("")
        elif a == 'color':
            p.color = abbr2color(request.POST['abbrev'])
            p.save()
            return HttpResponse("")
        else:
            return HttpResponseForbidden()

    return render(request, 'project.html', {
        'project': p})


@login_required
def projects(request):
    qs = Project.objects.filter(user=request.user)
    return render(request, 'projects.html', {'objects': qs})


@login_required
def add(request):
    if request.method == 'POST':
        f = CreateProjectForm(request.POST)
        if f.is_valid():
            p = f.save(commit=False)
            p.user = request.user
            p.save()
            return redirect('projects')
    else:
        f = CreateProjectForm()
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
                    return redirect('dashboard')
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
                    return redirect('dashboard')
        else:
            register_f = RegisterForm()
            login_f = LoginForm()
    else:
        register_f = RegisterForm()
        login_f = LoginForm()
    return render(request, 'register.html', {'register_form': register_f,
                                             'login_form': login_f})


def quick_track(request, selected_date=None):
    if selected_date is None:
        selected = get_user_date(request.user, selected_date).date()
    else:
        selected = get_user_date(request.user).date()
    if request.method == 'POST':
        f = QuickTrackForm(request.POST)
        if f.is_valid():
            t = f.save(commit=False)
            t.track_date = selected
            t.user = request.user
            t.save()
            messages.success(
                request,
                'Added {} hours to project "{}" at {}'.format(
                    t.hours,
                    t.project.name,
                    fdate(t.track_date)
                ))
            return redirect('dashboard')
    else:
        f = QuickTrackForm()
    f.fields['project'].queryset = Project.objects.filter(user=request.user)
    return render(request, 'quick_track.html', {
        'selected_date': selected, 'form': f})
