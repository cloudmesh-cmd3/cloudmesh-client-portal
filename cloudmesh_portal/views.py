# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pprint import pprint

from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaulttags import register
from sqlalchemy.orm import sessionmaker
from django_jinja import library


# noinspection PyPep8Naming
def Session():
    from aldjemy.core import get_engine
    engine = get_engine()
    _Session = sessionmaker(bind=engine)
    return _Session()


session = Session()

@library.global_function
def icon(name, color=None):
    if color is None:
        start = ""
        stop = ""
    else:
        start = '<font color="{}">'.format(color)
        stop = '</font>'
    if name in ["trash"]:
        icon = '<i class="fa fa-trash-o"></i>'
    elif name in ["cog"]:
        icon = '<i class="fa fa-cog"></i>'
    elif name in ["cog"]:
        icon = '<i class="fa fa-info"></i>'
    elif name in ["off"]:
        icon = '<i class="fa fa-power-off"></i>'
    elif name in ["on"]:
        icon = '<i class="fa fa-power-off"></i>'
    elif name in ["refresh"]:
        icon = '<i class="fa fa-refresh"></i>'
    elif name in ["chart"]:
        icon = '<i class="fa fa-bar-chart"></i>'
    elif name in ["desktop", "terminal"]:
        icon = '<i class="fa fa-desktop"></i>'
    elif name in ["info"]:
        icon = '<i class="fa fa-info-circle"></i>'
    elif name in ["launch"]:
        icon = '<i class="fa fa-rocket"></i>'
    else:
        icon = '<i class="fa fa-question-circle"></i>'
    return start + icon + stop

@library.global_function
def state_color(state):
    if state in ["R", "ACTIVE", "up", "active"]:
        return '<span class="label label-success"> {} </span>'.format(state)
    elif state in ["down", "down*", "fail"]:
        return '<span class="label label-danger"> {} </span>'.format(state)
    elif "error" in str(state):
        return '<span class="label label-danger"> {} </span>'.format(state)
    else:
        return '<span class="label label-default"> {} </span>'.format(state)


def message(msg):
    return HttpResponse("Message: %s." % msg)


# noinspection PyUnusedLocal
def cloudmesh_vclusters(request):
    return message("Not yet Implemented")


@register.filter
def get_item(dictionary, key):
    value = dictionary.get(key)
    if value is None:
        value = "-"
    return value


def dict_table(request, **kwargs):
    context = kwargs
    pprint(context)
    return render(request, 'cloudmesh_portal/dict_table.jinja', context)


def homepage(request):
    context = {
        'title': "Comet Home"
    }
    return render(request,
                  'cloudmesh_portal/home.jinja',
                  context)
