# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.storage import default_storage

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages

from django.shortcuts import render
from django.http import HttpResponse

from .forms import ContactForm, FilesForm, ContactFormSet
import json

from cloudmesh_client.comet.cluster import Cluster
from cloudmesh_client.comet.comet import Comet
from cloudmesh_client.cloud.hpc.hpc import Hpc

from django.template.defaulttags import register

from cloudmesh_client.common.ConfigDict import ConfigDict
from pprint import pprint


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def dict_table(request, title, data, order):
    context = {'title': title,
               'order': order,
               'data': data}
    return render(request, 'cloudmesh_portal/dict_table.html', context)


def comet_list(request):
    c = Comet.logon()
    data = json.loads(Cluster.simple_list(format="json"))

    order = ['id',
             'type',
             'cluster',
             'name',
             'ip']
    # 'kind']
    return (dict_table(request, "Comet List", data, order))


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

    return (dict_table(request, "Cloud List", data, headers))


def comet_list_queue(request):
    cluster = "comet"
    format = "json"
    order = [
        "jobid",
        # "nodelist",
        "name",
        "partition",
        "st",
        # "user",
        "time",
        "nodes",
    ]

    data = json.loads(Hpc.queue(cluster, format=format))
    print (data)

    return (dict_table(request, "Comet Queue", data, order))


# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, 'dummy.txt')


class HomePageView(TemplateView):
    template_name = 'cloudmesh_portal/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'This is a demo of a message.')
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
