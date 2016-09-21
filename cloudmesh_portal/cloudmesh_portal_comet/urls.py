from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^ll/', views.comet_ll, name='comet_ll'),
    url(r'^list/$', views.comet_list, name='comet_list'),
    url(r'^console/(?P<cluster>vc[0-9]+)/$', views.comet_console, name='comet_console'),
    url(r'^console/(?P<cluster>vc[0-9]+)/(?P<node>[-\w]+)/$', views.comet_console, name='comet_console'),
    url(r'^power/(?P<action>\w+)/(?P<cluster>vc[0-9]+)/$', views.comet_power, name='comet_power'),
    url(r'^power/(?P<action>\w+)/(?P<cluster>vc[0-9]+)/(?P<node>[-\w]+)/$', views.comet_power, name='comet_power'),
    url(r'^queue$', views.comet_list_queue, name='comet_list_queue'),
    url(r'^queue/info$', views.comet_info, name='comet_info'),

]
