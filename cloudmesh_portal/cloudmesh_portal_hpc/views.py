from __future__ import print_function
from __future__ import unicode_literals

import datetime
import json
from pprint import pprint

from cloudmesh_client.cloud.experiment import Experiment
from cloudmesh_client.cloud.hpc.BatchProvider import BatchProvider
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.util import path_expand
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaulttags import register
from django_jinja import library
from sqlalchemy.orm import sessionmaker

# noinspection PyPep8Naming
def Session():
    from aldjemy.core import get_engine
    engine = get_engine()
    _Session = sessionmaker(bind=engine)
    return _Session()


session = Session()


def dict_table(request, **kwargs):
    context = kwargs
    pprint(context)
    return render(request, 'cloudmesh_portal_hpc/dict_table.jinja', context)


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def index(request):
    context = {
        'title': ""
    }

    print (">>>>>", context)
    # template = loader.get_template('cloudmesh_portal_hpc/home.html')

    # print template

    # return HttpResponse(template.render(context, request))


    return render(request, 'cloudmesh_portal_hpc/home.jinja', context)



def hpc_run_list(request, count=None, cluster=None):
    cluster = "india"
    result = {}
    ids = Experiment.list(cluster, format="list")
    print (ids)
    for count in ids:
        result[count] = {
            "list": Experiment.list(cluster, id=count, format="list")
        }

    print (result)
    print (json.dumps(result, indent=4))

    order = ["list"]
    context = {
        "data": result,
        "title": "HPC Experiments on {}".format(cluster),
        "order": ["list"]
    }

    return render(request, 'cloudmesh_portal_hpc/run_table.jinja', context)


def hpc_list(request):
    clusters = ConfigDict(path_expand("~/.cloudmesh/cloudmesh.yaml"))["cloudmesh.hpc.clusters"]
    print (clusters)
    data = {}
    for cluster in clusters:
        data[cluster] = {
            "cluster": cluster,
            "test": "test"}
    order = ["cluster"]
    context = {
        "data": data,
        "title": "Clusters",
        "order": order,
    }
    return render(request, 'cloudmesh_portal_hpc/hpc_table.jinja', context)


def hpc_queue(request, cluster=None):
    output_format = "json"
    order = [
        "jobid",
        "user",
        "partition",
        "nodes",
        "st",
        "name",
        "nodelist",
        "time",
    ]
    provider = BatchProvider(cluster)
    data = json.loads(provider.queue(cluster, format=output_format))
    print (data)

    return dict_table(request,
                      title="Queues for {}".format(cluster),
                      data=data,
                      order=order)


def hpc_info(request, cluster=None):
    output_format = "json"
    order = [
        'partition',
        'nodes',
        'state',
        'avail',
        'timelimit',
        'cluster',
        'nodelist',
        # 'updated',
    ]
    provider = BatchProvider(cluster)

    data = json.loads(provider.info(cluster, format=output_format))
    print (data)

    return dict_table(request,
                      title="Info for {}".format(cluster),
                      data=data, order=order)



@library.global_function
def icon(name, color=None):
    if color is None:
        start = ""
        stop = ""
    else:
        start = '<font color="{}">'.format(color)
        stop = '</font>'
    if name in ["trash"]:
        icon_html = '<i class="fa fa-trash-o"></i>'
    elif name in ["cog"]:
        icon_html = '<i class="fa fa-cog"></i>'
    elif name in ["cog"]:
        icon_html = '<i class="fa fa-info"></i>'
    elif name in ["off"]:
        icon_html = '<i class="fa fa-power-off"></i>'
    elif name in ["on"]:
        icon_html = '<i class="fa fa-power-off"></i>'
    elif name in ["refresh"]:
        icon_html = '<i class="fa fa-refresh"></i>'
    elif name in ["chart"]:
        icon_html = '<i class="fa fa-bar-chart"></i>'
    elif name in ["desktop", "terminal"]:
        icon_html = '<i class="fa fa-desktop"></i>'
    elif name in ["info"]:
        icon_html = '<i class="fa fa-info-circle"></i>'
    elif name in ["launch"]:
        icon_html = '<i class="fa fa-rocket"></i>'
    else:
        icon_html = '<i class="fa fa-question-circle"></i>'
    return start + icon_html + stop


@library.global_function
def state_color(state):
    if state.lower() in ["r", "up", "active", 'yes', 'true']:
        return '<span class="label label-success"> {} </span>'.format(state)
    elif state.lower() in ["down", "down*", "fail", "false"]:
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


def portal_table(request, **kwargs):
    context = kwargs

    #debug user alerts
    for message in messages.get_messages(request):
        print(message)

    return render(request, 'cloudmesh_portal_hpc/portal_table.jinja', context)
