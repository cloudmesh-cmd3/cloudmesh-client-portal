from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^hpc/list/$', views.hpc_list, name='hpc_list'),
    url(r'^hpc/run/list/$', views.hpc_run_list, name='hpc_run_list'),
    url(r'^hpc/queue/(?P<cluster>\w+)/$', views.hpc_queue, name='hpc_queue'),
    url(r'^hpc/info/(?P<cluster>\w+)/$', views.hpc_info, name='hpc_info'),
]
