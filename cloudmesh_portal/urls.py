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
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from .views import HomePageView, StatusPageView, FormHorizontalView, \
    FormInlineView, PaginationView, FormWithFilesView, \
    DefaultFormView, MiscView, DefaultFormsetView, DefaultFormByFieldView, \
    comet_list, comet_list_queue,cloudmesh_clouds, cloudmesh_defaults, \
    cloudmesh_images, cloudmesh_flavors, cloudmesh_vms, cloudmesh_vclusters



from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    # Remove the sitemap in production
    url(r'^status', StatusPageView.as_view(), name='status'),

    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'flatpages': FlatPageSitemap}},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^formset$', DefaultFormsetView.as_view(), name='formset_default'),
    url(r'^form$', DefaultFormView.as_view(), name='form_default'),
    url(r'^form_by_field$', DefaultFormByFieldView.as_view(), name='form_by_field'),
    url(r'^form_horizontal$', FormHorizontalView.as_view(), name='form_horizontal'),
    url(r'^form_inline$', FormInlineView.as_view(), name='form_inline'),
    url(r'^form_with_files$', FormWithFilesView.as_view(), name='form_with_files'),
    url(r'^pagination$', PaginationView.as_view(), name='pagination'),
    url(r'^misc$', MiscView.as_view(), name='misc'),
    url(r'^cm/default/$', cloudmesh_defaults, name='cloudmesh_default'),
    url(r'^cm/image/$', cloudmesh_images, name='cloudmesh_image'),
    url(r'^cm/flavor/$', cloudmesh_flavors, name='cloudmesh_flavor'),
    url(r'^cm/vm/$', cloudmesh_vms, name='cloudmesh_vm'),
    url(r'^cm/vcluster/$', cloudmesh_vclusters, name='cloudmesh_vcluster'),
    url(r'^comet/overview', comet_ll, name='comet_ll'),
    url(r'^comet/list$', comet_list, name='comet_list'),
    url(r'^comet/queue$', comet_list_queue, name='comet_list_queue'),
    url(r'^clouds/$', cloudmesh_clouds, name='cloudmesh_clouds'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

