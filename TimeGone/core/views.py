from django.shortcuts import render
from models import Project


def index(request):
    return render(request, 'index.html', {'objects': Project.objects.all()})


