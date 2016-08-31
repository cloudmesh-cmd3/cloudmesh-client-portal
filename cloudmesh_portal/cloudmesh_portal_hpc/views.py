from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django_jinja import library


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def homepage(request):
    context = {
        'title': "HPC Home"
    }
    return render(request,
                  'cloudmesh_portal_hpc/home.html',
                  context)
