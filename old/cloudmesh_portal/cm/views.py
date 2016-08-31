from __future__ import unicode_literals
from __future__ import print_function
from pprint import pprint
import json

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.image import Image
from cloudmesh_client.cloud.flavor import Flavor
from cloudmesh_client.cloud.vm import Vm
from cloudmesh_client.cloud.launcher import Launcher
from cloudmesh_client.common.util import banner, path_expand
from django.contrib.messages import constants as message_constants

from ..views import dict_table
from ..views import get_item
from ..views import portal_table

def cloudmesh_launcher_table(request):
    launcher_config = ConfigDict(path_expand("~/.cloudmesh/cloudmesh_launcher.yaml"))

    context = {
        'recipies': launcher_config["cloudmesh.launcher.recipes"],
        'title': '<div><i class="fa fa-rocket"></i> Cloudmesh Launcher List </div>'
    }

    return render(request,
                  'cloudmesh_portal/launcher/mesh_launch_table.jinja',
                  context)


def cloudmesh_launcher(request):
    if request.method == 'POST':
        print ("HHHHHH", request.form.keys())
        for key in request.form.keys():
            print (key, ":", request.form[key])
    else:
        print ("HEY JUDE")

    launcher_config = ConfigDict(path_expand("~/.cloudmesh/cloudmesh_launcher.yaml"))

    context = {
        'recipies': launcher_config["cloudmesh.launcher.recipes"],
        'title': '<div><i class="fa fa-rocket"></i> Cloudmesh Launcher </div>'
    }

    pprint(context)

    return render(request,
                  'cloudmesh_portal/launcher/mesh_launch.jinja',
                  context)


def cloudmesh_launcher_start(request):
    parameters = dict(request.POST)
    for key in parameters:
        try:
            parameters[key] = parameters[key][0]
        except:
            pass
    if 'csrfmiddlewaretoken' in parameters:
        del parameters['csrfmiddlewaretoken']

    response = 'error'
    if parameters["name"]:
        name = parameters["name"]

        launcher_config = ConfigDict(path_expand("~/.cloudmesh/cloudmesh_launcher.yaml"))
        recipe = dict(launcher_config["cloudmesh.launcher.recipes"])[name]

        print(json.dumps(recipe, indent=4))

        response = "error"

        if recipe["script"]["type"] in ["sh", "shell"]:
            script = recipe["script"]["value"].format(**parameters)
            print (script)
            launcher = Launcher("shell")
            print (type(launcher))
            response = launcher.run(script=script)
            parameters["script"] = script

    else:
        parameters = "error"

    context = {
        'title': '<div><i class="fa fa-rocket"></i> Cloudmesh Launcher</div>',
        "response": response,
        "parameters": parameters,
    }

    return render(request,
                  'cloudmesh_portal/launcher/mesh_launch_response.jinja',
                  context)


def url(msg, link):
    print (locals())
    data = {
        'msg': msg,
        'link': link
    }
    return '<a href="{link}"> {msg} </a>'.format(**data)


def cloudmesh_clouds(request):
    config = ConfigDict(filename="cloudmesh.yaml")
    clouds = config["cloudmesh.clouds"]
    active = config["cloudmesh.active"]
    default = Default.cloud
    data = {}
    attributes = ['cm_label',
                  'cm_host',
                  'cm_heading',
                  'cm_type',
                  'cm_type_version']
    for cloud in clouds:
        name = {'cloud': cloud}
        data[cloud] = {}
        for attribute in attributes:
            data[cloud][attribute] = clouds[cloud][attribute]
        print (clouds[cloud]['cm_type'])
        if clouds[cloud]['cm_type'] == "ec2":
            data[cloud]['username'] = clouds[cloud]['credentials']['userid']
        elif clouds[cloud]['cm_type'] == "azure":
            data[cloud]['username'] = 'not implemented'
        elif clouds[cloud]['cm_type'] == "openstack":
            data[cloud]['username'] = clouds[cloud]['credentials'][
                'OS_USERNAME']
        if cloud in active:
            data[cloud]['active'] = 'yes'
        else:
            data[cloud]['active'] = 'no'
        if cloud in [default]:
            data[cloud]['default'] = 'yes'
        else:
            data[cloud]['default'] = 'no'
        data[cloud]['info'] = ", ".join([
            url('d', '/cm/cloud/{cloud}/'.format(**name)),
            url('i', '/cm/image/{cloud}/'.format(**name)),
            url('f', '/cm/flavor/{cloud}/'.format(**name)),
            url('v', '/cm/vm/{cloud}/'.format(**name))])

    order = [
        'default',
        'active',
        'cm_label',
        'info',
        'username',
        'cm_host',
        'cm_heading',
        'cm_type',
        'cm_type_version'
    ]
    header = [
        'Default',
        'Active',
        'Label',
        'Info',
        'Username',
        'Host',
        'Description',
        'Type',
        'Version'
    ]

    pprint(data)

    context = {
        'data': data,
        'title': "Cloud List",
        'order': order,
        'header': header,
    }
    return render(request,
                  'cloudmesh_portal/dict_table.jinja',
                  context)


def cloudmesh_cloud(request, cloud=None):
    if cloud is None:
        cloud = Default.cloud
    config = ConfigDict(filename="cloudmesh.yaml")
    cloud_config = dict(config["cloudmesh.clouds"][cloud])
    active = cloud in config["cloudmesh.active"]
    default = Default.cloud

    if 'OS_PASSWORD' in cloud_config['credentials']:
        cloud_config['credentials']['OS_PASSWORD'] = '********'
    context = {
        'data': cloud_config,
        'title': "Cloud {cm_heading}".format(**cloud_config),
    }
    return render(request,
                  'cloudmesh_portal/cm/cloud_table.jinja',
                  context)


#
# CLOUDMESH DEFAULTS
#


def cloudmesh_defaults(request):
    data = json.loads(Default.list(output='json'))

    print("RESULT DEFAULT",data)

    order = [
        'category',
        'name',
        'value',
        'project',
        'user',
    ]
    header = [
        'Category',
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


def cloudmesh_images(request, cloud=None):
    banner("images")
    if cloud is None:
        cloud = Default.cloud
    # TODO: make the cloudname a parameter
    data = Image.list(cloud, format='dict')
    print (json.dumps(data, indent=4))
    # TODO set proper columns
    order = [
        'cm_id',
        'name',
        'category',
        'minDisk',
        'minRam',
        'os_image_size',
        'progress',
        'project',
        'status',
    ]
    return (dict_table(request,
                       title="Cloudmesh Images {}".format(cloud),
                       data=data,
                       order=order))


def cloudmesh_flavors(request, cloud=None):
    if cloud is None:
        cloud = Default.cloud
    data = Flavor.list(cloud, format='dict')
    print (json.dumps(data, indent=4))


    order = [
        'cm_id',
        'name',
        'category',
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
    return dict_table(request,
                      title="Cloudmesh Flavors {}".format(cloud),
                      data=data, order=order)


def cloudmesh_vms(request, cloud=None):

    if cloud is None:
        cloud = Default.cloud

        data = Vm.list(category=cloud, output='dict')
        print("cloud debug",cloud)
        order = ['cm_id',
                     'uuid',
                     'label',
                     'status',
                     'static_ip',
                     'floating_ip',
                     'project',
                     'category']

    print("HERE*************************")
    return portal_table(request,
                              title="Cloudmesh VMs {}".format(cloud),
                              data=data, order=order)



def cloudmesh_refresh(request, action=None, cloud=None):
    if action is None:
        action = ['image', 'flavor', 'vm']
    else:
        action = [action]

    if cloud is None:
        cloud = Default.cloud
        # TODO: should actually be all active clouds

    data = Vm.list(cloud=cloud, output_format='dict')
    print (json.dumps(data, indent=4))
    order = ['cm_id',
             'uuid',
             'label',
             'status',
             'static_ip',
             'floating_ip',
             'key_name',
             'project',
             'user',
             'category']

    return dict_table(request,
                      title="Cloudmesh VMs {}".format(cloud),
                      data=data, order=order)

def cloudmesh_refresh_db(request, action=None, cloud=None):

    if action is None:
        action = ['image']
    else:
        action = [action]

    print("******DEBUG*********")
    print("ACTION IS:",action)
    print("******DEBUG*********")

    if cloud is None:
        cloud = Default.cloud
    # TODO: make the cloudname a parameter
    data = Image.refresh(cloud)

    print("REFRESH IMAGE DATA",data)

    data = Image.list(cloud, format='dict')
    print(json.dumps(data, indent=4))
    # TODO set proper columns
    order = [
        'cm_id',
        'name',
        'category',
        'minDisk',
        'minRam',
        'os_image_size',
        'progress',
        'project',
        'status',
    ]

    return (dict_table(request,
                       title="Cloudmesh Images {}".format(cloud),
                       data=data,
                       order=order))

def cloudmesh_refresh_vm(request, action=None, cloud=None):

    if cloud is None:
        cloud = Default.cloud
    # TODO: make the cloudname a parameter
    data = Vm.refresh(cloud=cloud)

    messages.info(request,'Database Refresh was successful!')

    return redirect('cloudmesh_vm')

def cloudmesh_vm_action(request,action=None,cloud=None):


    print("******$$$$$$$$$$$$$*********")
    print("REQUEST")
    print("******$$$$$$$$$$$$$*********")

    if 'stop_vm' in request.POST:

        try:

            terminate_id=[]

            if request.method == "POST":
                terminate_id = request.POST.getlist('vm_id')

            print("******DEBUG*********")
            print("STOP VM:", terminate_id)
            print("******DEBUG*********")

            if cloud is None:
                cloud = Default.cloud

            for label in terminate_id:
                server_name=label
                print("server_name",server_name)
                Vm.stop(cloud=cloud,servers=[server_name])

            messages.success(request,'VM Stopped Successfully!')

            return redirect('cloudmesh_vm')

        except Exception:

            messages.error(request,'WARNING! Cannot stop a VM already in stopped state!')

            return redirect('cloudmesh_vm')


    if 'start_vm' in request.POST:

        try:

            start_id=[]

            if request.method == "POST":
                start_id = request.POST.getlist('vm_id')

            print("******DEBUG*********")
            print("START VM:", start_id)
            print("******DEBUG*********")

            if cloud is None:
                cloud = Default.cloud

            for label in start_id:
                server_name=label
                print("VM name",server_name)
                Vm.start(cloud=cloud,servers=[server_name])

            messages.success(request,'VM Started Successfully!')

            return redirect('cloudmesh_vm')

        except Exception:

            messages.error(request, 'WARNING! Cannot start a VM already in stopped state!')

            return redirect('cloudmesh_vm')

    if 'boot_vm' in request.POST:

        messages.error(request,'Feature Not Implemented!')

        return redirect('cloudmesh_vm')

    if 'delete_vm' in request.POST:

        messages.error(request,'Feature Not Implemented!')

        return redirect('cloudmesh_vm')