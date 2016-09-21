from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^launcher/list$', views.cloudmesh_launcher_table, name='cloudmesh_launcher_table'),
    url(r'^launcher/$', views.cloudmesh_launcher, name='cloudmesh_launcher'),
    url(r'^launcher/start/$', views.cloudmesh_launcher_start, name='cloudmesh_launcher_start'),
    url(r'^clouds/$', views.cloudmesh_clouds, name='cloudmesh_clouds'),
    url(r'^cloud/(?P<cloud>\w+)/$', views.cloudmesh_cloud, name='cloudmesh_cloud'),
    url(r'^default/$', views.cloudmesh_defaults, name='cloudmesh_default'),
    url(r'^refresh/(?P<action>\w+)/(?P<cloud>\w+)/$', views.cloudmesh_refresh, name='cloudmesh_refresh'),
    url(r'^image/refresh/$', views.cloudmesh_refresh_db, name='cloudmesh_refresh_db'),
    url(r'^flavor/refresh/$', views.cloudmesh_refresh_db, name='cloudmesh_refresh_db'),
    url(r'^vm/refresh/$', views.cloudmesh_refresh_vm, name='cloudmesh_refresh_vm'),
    url(r'^vm/vm_action/$', views.cloudmesh_vm_action, name='cloudmesh_vm_action'),
    url(r'^image/$', views.cloudmesh_images, name='cloudmesh_image'),
    url(r'^image/(?P<cloud>\w+)/$', views.cloudmesh_images, name='cloudmesh_image'),
    url(r'^flavor/$', views.cloudmesh_flavors, name='cloudmesh_flavor'),
    url(r'^flavor/(?P<cloud>\w+)/$', views.cloudmesh_flavors, name='cloudmesh_flavor'),
    url(r'^vm/$', views.cloudmesh_vms, name='cloudmesh_vm'),
    url(r'^vm/(?P<info>\w+)/$', views.cloudmesh_vms, name='cloudmesh_vm'),
    url(r'^vm/(?P<cloud>\w+)/$', views.cloudmesh_vms, name='cloudmesh_vm'),
    url(r'^vcluster/$', views.cloudmesh_vclusters, name='cloudmesh_vcluster'),

]
