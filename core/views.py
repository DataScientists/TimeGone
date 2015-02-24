from __future__ import division

import json
import logging

from datetime import date, timedelta

import arrow

from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.db.utils import IntegrityError
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseRedirect)
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import formats
from django.views.decorators.http import require_http_methods

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from constants import abbr2color, COLORS, color2abbr
from forms import (
    RegisterForm, LoginForm, TrackTimeForm, ProjectForm,
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


def parse_date(request, k):
    year, month, day = map(int, request.GET[k].split('-'))
    return date(year, month, day)


@login_required
def report(request):
    if 'start' in request.GET and 'end' in request.GET:
        start = parse_date(request, 'start')
        end = parse_date(request, 'end')
    else:
        a = get_user_date(request.user)
        start = a.date()
        end = start + timedelta(days=1)

    qs = TrackedTime.objects.filter(
        user=request.user,
        track_date__gte=start,
        track_date__lte=end).order_by('id')
    projects = list((list(x) for x in
                     Project.objects.filter(user=request.user).
                     order_by('-name').values_list('id', 'name')))
    tracked_time = list((json.dumps({
        # remove button
        'delete_url': reverse('time_delete', args=(x.id,)),
        # project
        'project_name': x.project.name,
        'project_pk': x.id,
        'project_url': reverse('time_project_api', args=(x.id,)),
        'projects': projects,
        # hours
        'hours': x.hours,
        'hours_url': reverse('time_hours_api', args=(x.id,)),
        # description
        'description': x.description,
        'description_url': reverse('time_description_api', args=(x.id,)),
        # track date
        'track_date': fdate(x.track_date),
        'track_date_url': reverse('time_track_date_api', args=(x.id,))
    }) for x in qs))
    return render(request, "report.html", {
        'start': fdate(start),
        'end': fdate(end),
        'tracked_time': tracked_time,
        'next': request.get_full_path()})


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
                    obj.hours, obj.description, fdate(obj.track_date)))
            return redirect('projects')
    else:
        f = TrackTimeForm()
    return render(request, 'track.html', {'form': f, 'project': project})


def get_graph(user, date):
    qs = TrackedTime.objects.filter(user=user, track_date=date)\
                            .values('project', 'project__name',
                                    'project__color', 'hours').order_by('pk')
    return json.dumps({'g': list(qs)})


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
    dates = []
    dates.insert(0, today)
    yesterday = today - timedelta(days=1)
    dates.insert(1, yesterday)
    for i in range(2, 7):
        last_seven = today - timedelta(days=i)
        dates.insert(i, last_seven)

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


def prepare_colored_projects(projects):
    result = []
    colors = set(COLORS)
    for p in projects:
        result.append((color2abbr(p.color), (p.name, p.id)))
        if p.color in colors:
            colors.remove(p.color)
    for c in colors:
        result.append((color2abbr(c), None))
    return json.dumps({'g': result})


def quick_track_form(projects, get, post=None):
    if post is not None:
        args = (post,)
    else:
        args = ()
    if 'pid' in get:
        kwargs = dict(initial={'project': int(get['pid'])})
    else:
        kwargs = {}
    f = QuickTrackForm(*args, **kwargs)
    f.fields['project'].queryset = projects
    return f


def selected_date_from_get(request):
    if 'date' in request.GET:
        selected = get_user_date(request.user, request.GET['date']).date()
    else:
        selected = get_user_date(request.user).date()
    return selected


@login_required
def quick_track(request):
    projects = Project.objects.filter(user=request.user)\
                              .annotate(Sum('trackedtime__hours'))\
                              .order_by('-trackedtime__hours__sum')
    if request.method == 'POST':
        f = quick_track_form(projects, request.GET, request.POST)
        if f.is_valid():
            t = f.save(commit=False)
            t.track_date = selected_date_from_get(request)
            t.user = request.user
            t.save()
            messages.success(
                request,
                'Added {} hours to project "{}" at {}'.format(
                    t.hours,
                    t.project.name,
                    fdate(t.track_date)
                ))
            today = get_user_date(request.user).date()
            if t.track_date == today:
                return redirect('dashboard')
            else:
                url = reverse('dashboard') + '?date=%s' % fdate(t.track_date)
                return HttpResponseRedirect(url)
    else:
        f = quick_track_form(projects, request.GET)
    return render(request, 'quick_track.html', {
        'form': f,
        'colored': prepare_colored_projects(projects)})


@require_http_methods(['POST'])
@login_required
def delete_tracked_time(request, obj_id):
    x = get_object_or_404(
        TrackedTime.objects.filter(user=request.user),
        id=obj_id)
    x.delete()
    return redirect(request.POST['next'])


@login_required
def create(request):
    if 'color' in request.GET:
        color = abbr2color(request.GET['color'])
    else:
        color = None
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.user = request.user
            p.save()
            if 'back' in request.GET:
                return redirect(request.GET['back'] + '?pid=%s' % p.id)
            else:
                return redirect('project', p.id)
    else:
        if color is not None:
            form = ProjectForm(initial={'color': color})
        else:
            form = ProjectForm()
    return render(request, 'add.html', {'form': form,
                                        'action': request.get_full_path})


@login_required
@require_http_methods(['POST'])
def time_delete(request, pk):
    tt = get_object_or_404(TrackedTime, user=request.user, pk=pk)
    tt.delete()
    return HttpResponse('')


@require_http_methods(['POST'])
@login_required
@csrf_exempt
def time_project_api(request, pk):
    tt = get_object_or_404(TrackedTime, user=request.user, pk=pk)
    project = Project.objects.get(user=request.user,
                                  pk=request.POST['pk'])
    tt.project = project
    tt.save()
    return HttpResponse('')


@require_http_methods(['POST'])
@login_required
@csrf_exempt
def time_hours_api(request, pk):
    tt = get_object_or_404(TrackedTime, user=request.user, pk=pk)
    tt.hours = request.POST['hours']
    tt.save()
    return HttpResponse('')


@require_http_methods(['POST'])
@login_required
@csrf_exempt
def time_description_api(request, pk):
    tt = get_object_or_404(TrackedTime, user=request.user, pk=pk)
    tt.description = request.POST['description']
    tt.save()
    return HttpResponse('')


@require_http_methods(['POST'])
@login_required
@csrf_exempt
def time_track_date_api(request, pk):
    tt = get_object_or_404(TrackedTime, user=request.user, pk=pk)
    tt.track_date = request.POST['track_date']
    tt.save()
    return HttpResponse('')
