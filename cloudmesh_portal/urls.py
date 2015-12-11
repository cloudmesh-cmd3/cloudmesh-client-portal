"""comet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.contrib import admin
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


from .comet.views import comet_list, comet_ll, comet_list_queue, \
    comet_info, comet_status, comet_console, comet_power

from .views import homepage, cloudmesh_vclusters
from .cm.views import cloudmesh_defaults, cloudmesh_images, \
    cloudmesh_flavors, cloudmesh_vms, cloudmesh_clouds, \
    cloudmesh_launcher, cloudmesh_launcher_start, cloudmesh_launcher_table, cloudmesh_refresh, \
    cloudmesh_cloud


from .hpc.views import hpc_list, hpc_info, hpc_queue, hpc_run_list

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    # Remove the sitemap in production
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'flatpages': FlatPageSitemap}},
        name='django.contrib.sitemaps.views.sitemap'),
    #
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^$', homepage, name='home'),
    url(r'^hpc/list/$', hpc_list, name='hpc_list'),
    url(r'^hpc/run/list/$', hpc_run_list, name='hpc_run_list'),
    url(r'^hpc/queue/(?P<cluster>\w+)/$', hpc_queue, name='hpc_queue'),
    url(r'^hpc/info/(?P<cluster>\w+)/$', hpc_info, name='hpc_info'),
    url(r'^cm/launcher/list$', cloudmesh_launcher_table, name='cloudmesh_launcher_table'),
    url(r'^cm/launcher/$', cloudmesh_launcher, name='cloudmesh_launcher'),
    url(r'^cm/launcher/start/$', cloudmesh_launcher_start, name='cloudmesh_launcher_start'),
    url(r'^cm/clouds/$', cloudmesh_clouds, name='cloudmesh_clouds'),
    url(r'^cm/cloud/(?P<cloud>\w+)/$', cloudmesh_cloud, name='cloudmesh_cloud'),
    url(r'^cm/default/$', cloudmesh_defaults, name='cloudmesh_default'),
    url(r'^cm/refresh/(?P<action>\w+)/(?P<cloud>\w+)/$', cloudmesh_refresh, name='cloudmesh_refresh'),
    url(r'^cm/image/$', cloudmesh_images, name='cloudmesh_image'),
    url(r'^cm/image/(?P<cloud>\w+)/$', cloudmesh_images, name='cloudmesh_image'),
    url(r'^cm/flavor/$', cloudmesh_flavors, name='cloudmesh_flavor'),
    url(r'^cm/flavor/(?P<cloud>\w+)/$', cloudmesh_flavors, name='cloudmesh_flavor'),
    url(r'^cm/vm/$', cloudmesh_vms, name='cloudmesh_vm'),
    url(r'^cm/vm/(?P<cloud>\w+)/$', cloudmesh_vms, name='cloudmesh_vm'),
    url(r'^cm/vcluster/$', cloudmesh_vclusters, name='cloudmesh_vcluster'),
    url(r'^comet/status', comet_status, name='comet_status'),
    url(r'^comet/ll', comet_ll, name='comet_ll'),
    url(r'^comet/list$', comet_list, name='comet_list'),
    url(r'^comet/console/(?P<cluster>vc[0-9]+)/$', comet_console, name='comet_console'),
    url(r'^comet/console/(?P<cluster>vc[0-9]+)/(?P<node>[-\w]+)/$', comet_console, name='comet_console'),
    url(r'^comet/power/(?P<action>\w+)/(?P<cluster>vc[0-9]+)/$', comet_power, name='comet_power'),
    url(r'^comet/power/(?P<action>\w+)/(?P<cluster>vc[0-9]+)/(?P<node>[-\w]+)/$', comet_power, name='comet_power'),
    url(r'^comet/queue$', comet_list_queue, name='comet_list_queue'),
    url(r'^comet/queue/info$', comet_info, name='comet_info'),
    url(r'^clouds/$', cloudmesh_clouds, name='cloudmesh_clouds'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
]

