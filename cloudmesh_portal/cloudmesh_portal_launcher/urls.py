from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^launcher/list$', views.cloudmesh_launcher_table, name='cloudmesh_launcher_table'),
    url(r'^launcher/$', views.cloudmesh_launcher, name='cloudmesh_launcher'),
    url(r'^launcher/start/$', views.cloudmesh_launcher_start, name='cloudmesh_launcher_start'),

]
