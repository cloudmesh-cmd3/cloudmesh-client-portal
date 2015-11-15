# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pprint import pprint
import json

from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from cloudmesh_client.comet.cluster import Cluster
from cloudmesh_client.comet.comet import Comet
from cloudmesh_client.cloud.hpc.hpc import Hpc
from django.template.defaulttags import register
from cloudmesh_client.common.ConfigDict import ConfigDict
from sqlalchemy.orm import sessionmaker
from cloudmesh_client.db.model import IMAGE
from cloudmesh_client.cloud.default import Default
from cloudmesh_client.cloud.image import Image
from cloudmesh_client.cloud.flavor import Flavor
from cloudmesh_client.cloud.vm import Vm



from charts import Chart
from .forms import ContactForm, FilesForm, ContactFormSet


def Session():
    from aldjemy.core import get_engine
    engine = get_engine()
    _Session = sessionmaker(bind=engine)
    return _Session()


session = Session()


def message(msg):
    return HttpResponse("Message: %s." % msg)


def cloudmesh_vclusters(request):
    return message("Not yet Implemented")



@register.filter
def get_item(dictionary, key):
    value = dictionary.get(key)
    if value is None:
        value = "-"
    return value


def dict_table(request, title, data, order=None, header=None):
    context = {'title': title,
               'order': order,
               'data': data}
    if header is not None:
        context['header'] = header
    return render(request, 'cloudmesh_portal/dict_table.jinja', context)


class StatusPageView(TemplateView):
    #template_name = 'cloudmesh_portal/status.html'
    template_name = 'cloudmesh_portal/status.jinja'

    context = {}
    c = Comet.logon()
    data = json.loads(Cluster.simple_list(format="json"))
    pprint(data)
    print (type(data))

    clusters = []
    for key in data:
        total = data[key]["nodes"]
        name = data[key]["name"]
        if name == "comet-fe1":
            name = "free"
        cluster = {
            "name": name,
            "total": total,
            "status": {
                'active': 0,
                'nostate': 0,
                'down': 0,
                'pending': 0,
                'unkown': total
            }
        }
        clusters.append(cluster)

    details = json.loads(Cluster.list(format="json"))

    counter = {}
    for id in data.keys():
        counter[id] = {
            'name': None,
            'total': 0,
            'status': {
                'unkown': 0,
                'active': 0,
                'down': 0,
                'pending': 0,
                'nostate': 0,
                'nostate-error': 0
            }
        }

    print (counter)
    for key, node in details.items():

        if node['kind'] == 'compute':

            name = node['cluster']
            state = node['state']

            if state in [None, 'None']:
                state = 'unkown'

            print ("SSSSSSS", state, name, node['kind'])

            element = counter[name]
            counter[name]['status'][state] += 1
            counter[name]['total'] += 1
            counter[name]['name'] = name

    #
    # delete the free nodes for now
    #

    for count in counter:
        if count != "comet-fe1":
            counter['comet-fe1']['total'] = counter['comet-fe1']['total'] - \
                                            counter[count]['total']

    counter['comet-fe1']['name'] = 'free'
    counter_list = []
    for key, cluster in counter.items():
        counter_list.append(cluster)

    # context["clusters"] = counter_list

    Chart.cluster_overview_pie(counter_list, filename='pie.svg')

    #
    # delete the overall count
    #
    del counter['comet-fe1']
    counter_list = []
    for key, cluster in counter.items():
        counter_list.append(cluster)

    Chart.cluster_overview_pie_vector(counter_list, filename='pie_vector.svg')
    Chart.cluster_overview_radar(counter_list, filename='radar.svg')


    context['pid'] = str(Comet.find_tunnel())
    context['tunnel'] = str(Comet.is_tunnel())

    def get_context_data(self, **kwargs):
        context = super(StatusPageView, self).get_context_data(**kwargs)
        # messages.info(self.request, 'This is a demo of a message.')
        return context


def comet_ll(request):
    c = Comet.logon()
    data = json.loads(Cluster.simple_list(format="json"))

    # pprint(type(data), data)
    order = [
        "name",
        "project",
        "nodes",
        "computes",
        "frontend name",
        "frontend state",
        "frontend type",
        "frontend rocks_name",
        "description",
    ]
    header = [
        "Name",
        "Project",
        "Count",
        "Nodes",
        "Frontend (Fe)",
        "State (Fe)",
        "Type (Fe)",
        "Rocks name (Fe)",
        "Description",
    ]

    return (dict_table(request, "Comet List", data, order=order))


def comet_list(request):
    c = Comet.logon()
    data = json.loads(Cluster.list(format="json"))

    dictionary = {}

    for item in data.values():
        dictionary[item["name"]] = item

    order = [
        "name",
        "state",
        "kind",
        "type",
        "ip",
        "rocks_name",
        "cpus",
        "cluster",
        "host",
        "memory",
    ]

    return (dict_table(request, "Comet List", dictionary, order=order))


def cloudmesh_clouds(request):
    config = ConfigDict(filename="cloudmesh.yaml")
    clouds = config["cloudmesh.clouds"]
    data = {}
    attributes = ['cm_host', 'cm_label', 'cm_heading', 'cm_type',
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
                'OS_PASSWORD']

    headers = ['username']
    headers.extend(attributes)

    return (dict_table(request, "Cloud List", data, order=headers))


def comet_list_queue(request):
    cluster = "comet"
    format = "json"
    order = [
        "jobid",
        "nodelist",
        "name",
        "partition",
        "st",
        "user",
        "time",
        "nodes",
    ]

    data = json.loads(Hpc.queue(cluster, format=format))
    print (data)

    return (dict_table(request, "Comet Queue", data, order=order))


# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, 'dummy.txt')


class HomePageView(TemplateView):
    template_name = 'cloudmesh_portal/home.jinja'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # messages.info(self.request, 'This is a demo of a message.')
        return context


class DefaultFormsetView(FormView):
    template_name = 'cloudmesh_portal/formset.html'
    form_class = ContactFormSet


class DefaultFormView(FormView):
    template_name = 'cloudmesh_portal/form.html'
    form_class = ContactForm


class DefaultFormByFieldView(FormView):
    template_name = 'cloudmesh_portal/form_by_field.html'
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = 'cloudmesh_portal/form_horizontal.html'
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = 'cloudmesh_portal/form_inline.html'
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = 'cloudmesh_portal/form_with_files.html'
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'vertical')
        return context

    def get_initial(self):
        return {
            'file4': fieldfile,
        }


class PaginationView(TemplateView):
    template_name = 'cloudmesh_portal/pagination.html'

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(10000):
            lines.append('Line %s' % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get('page')
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of
            # results.
            show_lines = paginator.page(paginator.num_pages)
        context['lines'] = show_lines
        return context


class MiscView(TemplateView):
    template_name = 'cloudmesh_portal/misc.html'
