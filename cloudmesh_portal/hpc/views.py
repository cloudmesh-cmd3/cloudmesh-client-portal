from __future__ import unicode_literals
import json

from cloudmesh_client.cloud.hpc.hpc import Hpc
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_base.util import banner, path_expand
from cloudmesh_portal.views import dict_table


from django.shortcuts import render

def hpc_list(request):
    clusters = ConfigDict(path_expand("~/.cloudmesh/cloudmesh.yaml"))["cloudmesh.hpc"]
    print clusters
    data={}
    for cluster in clusters:
        data[cluster] = {
            "cluster": cluster,
            "test": "test"}
    order = ["cluster"]
    context = {
        "data" : data,
        "title": "Clusters",
        "order": order,
    }
    return render(request, 'cloudmesh_portal/hpc_table.jinja', context)

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

    data = json.loads(Hpc.queue(cluster, format=output_format))
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
    data = json.loads(Hpc.info(cluster, format=output_format))
    print (data)

    return dict_table(request,
                      title="Info for {}".format(cluster),
                      data=data, order=order)

