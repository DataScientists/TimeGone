from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from forms import RegisterForm
from models import Project
from django.db.utils import IntegrityError

@login_required
def index(request):
    qs = Project.objects.filter(user=request.user)
    return render(request, 'index.html', {'objects': qs})

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password'])
            except IntegrityError, e:
                if 'username' in str(e):
                    form.add_error('username', 'Username is taken')
                elif 'email' in str(e):
                    form.add_error('email', 'Email is already registered')
                else:
                    raise e
            else:
                user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'])
                login(request, user)
                return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
