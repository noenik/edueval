from django.shortcuts import render
from .models import Course


def mng_home(request):
    courses = Course.objects.all()
    return render(request, 'management/mng_home.html', {'courses': courses})
