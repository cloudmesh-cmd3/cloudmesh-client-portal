from __future__ import unicode_literals
from pprint import pprint
import json

from django.shortcuts import render
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.cloud.default import Default
from cloudmesh_client.cloud.image import Image
from cloudmesh_client.cloud.flavor import Flavor
from cloudmesh_client.cloud.vm import Vm
from cloudmesh_client.cloud.launcher import Launcher
from cloudmesh_base.util import banner, path_expand

from ..views import dict_table


def cloudmesh_launcher(request):
    if request.method == 'POST':
        print "HHHHHH", request.form.keys()
        for key in request.form.keys():
            print key, ":", request.form[key]
    else:
        print "HEY JUDE"

    launcher_config = ConfigDict(path_expand("~/.cloudmesh/cloudmesh_launcher.yaml"))

    context = {
        'recipies': launcher_config["cloudmesh.launcher.recipes"],
        'title': '<div><i class="fa fa-rocket"></i> Cloudmesh Launcher </div>'
    }

    pprint (context)

    return render(request,
                  'cloudmesh_portal/mesh_launch.jinja',
                  context)


def cloudmesh_launcher_start(request):
    parameters = dict(request.POST)

    if 'csrfmiddlewaretoken' in parameters:
        del parameters['csrfmiddlewaretoken']

    launcher = Launcher()

    response = launcher.run()

    context = {
        'title': '<div><i class="fa fa-rocket"></i> Cloudmesh Launcher</div>',
        "response": response,
        "parameters": parameters,
    }

    return render(request,
                  'cloudmesh_portal/mesh_launch2.jinja',
                  context)



def cloudmesh_clouds(request):
    config = ConfigDict(filename="cloudmesh.yaml")
    clouds = config["cloudmesh.clouds"]
    data = {}
    attributes = ['cm_label',
                  'cm_host',
                  'cm_heading',
                  'cm_type',
                  'cm_type_version']

    for cloud in clouds:
        data[cloud] = {}
        for attribute in attributes:
            data[cloud][attribute] = clouds[cloud][attribute]
        print clouds[cloud]['cm_type']
        if clouds[cloud]['cm_type'] == "ec2":
            data[cloud]['username'] = clouds[cloud]['credentials']['userid']
        elif clouds[cloud]['cm_type'] == "azure":
            data[cloud]['username'] = 'not implemented'
        elif clouds[cloud]['cm_type'] == "openstack":
            data[cloud]['username'] = clouds[cloud]['credentials'][
                'OS_USERNAME']

    order = [
        'cm_label',
        'username',
        'cm_host',
        'cm_heading',
        'cm_type',
        'cm_type_version'
    ]

    pprint(data)

    context = {
        'data': data,
        'title': "Cloud List",
        'order': order,
    }
    return render(request,
                  'cloudmesh_portal/dict_table.jinja',
                  context)


#
# CLOUDMESH DEFAULTS
#


def cloudmesh_defaults(request):
    data = json.loads(Default.list(format='json'))

    order = [
        'cloud',
        'name',
        'value',
        'project',
        'user',
    ]
    header = [
        'Cloud',
        'Variable',
        'Value',
        'Project',
        'User',
    ]

    return (dict_table(request,
                       title="Cloudmesh Default",
                       data=data,
                       header=header,
                       order=order))


def cloudmesh_images(request):
    banner("images")
    # TODO: make the cloudname a parameter
    data = Image.list("juno", format='dict')
    print json.dumps(data, indent=4)
    # TODO set proper columns
    order = [
        'id',
        'name',
        'cloud',
        'minDisk',
        'minRam',
        'os_image_size',
        'progress',
        'project',
        'status',
    ]
    return (dict_table(request,
                       title="Cloudmesh Images",
                       data=data,
                       order=order))


def cloudmesh_flavors(request):
    data = Flavor.list("juno", format='dict')
    print json.dumps(data, indent=4)

    order = [
        'id',
        'name',
        'cloud',
        'disk',
        'os_flavor_acces',
        'os_flv_disabled',
        'os_flv_ext_data',
        'project',
        'ram',
        'rxtx_factor',
        'swap',
        'vcpus',
    ]
    return dict_table(request, title="Cloudmesh Flavors", data=data, order=order)


def cloudmesh_vms(request):
    data = Vm.list(cloud="juno", output_format='dict')
    print json.dumps(data, indent=4)
    order = ['id',
             'uuid',
             'label',
             'status',
             'static_ip',
             'floating_ip',
             'key_name',
             'project',
             'user',
             'cloud']
    return dict_table(request, title="Cloudmesh VMs", data=data, order=order)
