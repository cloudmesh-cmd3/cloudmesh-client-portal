from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django_jinja import library
from django.template import loader

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def home(request):
    context = {
        'title': ""
    }

    print ">>>>>", context
    # template = loader.get_template('cloudmesh_portal_hpc/home.html')

    # print template

    # return HttpResponse(template.render(context, request))


    return render(request, 'cloudmesh_portal_hpc/home.jinja', context)