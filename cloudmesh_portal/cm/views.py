import json

from cloudmesh_client.cloud.default import Default
from cloudmesh_client.cloud.image import Image
from cloudmesh_client.cloud.flavor import Flavor
from cloudmesh_client.cloud.vm import Vm
from cloudmesh_base.util import banner
from django.shortcuts import render


def dict_table(request, title, data, order=None, header=None):
    context = {'title': title,
               'order': order,
               'data': data}
    if header is not None:
        context['header'] = header
    return render(request, 'cloudmesh_portal/dict_table.html', context)


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
                       "Cloudmesh Default",
                       data,
                       header=header,
                       order=order))


def cloudmesh_images(request):
    banner("images")
    # TODO: make the cloudname a parameter
    data = Image.list("juno", format='dict')
    print json.dumps(data, indent=4)
    # TODO set proper columns
    order = ['kind',
             'name',
             'value',
             'project',
             'user',
             'type',
             'id',
             'cloud']
    return (dict_table(request, "Cloudmesh Images", data, order=order))


def cloudmesh_flavors(request):
    data = Flavor.list("juno", format='dict')
    print json.dumps(data, indent=4)
    order = ['kind',
             'name',
             'value',
             'project',
             'user',
             'type',
             'id',
             'cloud']
    return (dict_table(request, "Cloudmesh Flavors", data, order=order))


def cloudmesh_vms(request):
    data = Vm.list(format='dict')
    print json.dumps(data, indent=4)
    order = ['kind',
             'name',
             'value',
             'project',
             'user',
             'type',
             'id',
             'cloud']
    return (dict_table(request, "Cloudmesh VMs", data, order=order))
