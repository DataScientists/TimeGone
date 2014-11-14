from django.auth.decorators import login_required
from django.shortcuts import render, redirect

from forms import RegiserForm
from models import Project


@login_required
def index(request):
    return render(request, 'index.html', {'objects': Project.objects.all()})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST.data)
        if form.is_valid():
            user = User.objects.create(username=form.cleaned_data['username'])
            user.set_password(form.cleaned_data['password'])
            user.save()
            # login user
            # redirect
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
