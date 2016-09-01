README.rstCloudmesh TBD
=============

Cloudmesh TBD allows you to add  TBD
to your django applications,

Detailed documentation will bi in the "docs" directory.

Quick start
-----------

1. Add "cloudmesh hpc" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'cloudmesh_portal_TBD',
    ]

2. Include the URLconf in your project urls.py like this::

    url(r'^TBD/', include('TBD.urls')),


3. Make sure you include the HPC queues you like to work with in the
   ~/.cloudmesh/cloudmesh.yaml file. Please see the "cloudmesh client"
   documentation in github:

   * http://cloudmesh.github.io/client/
   
3. Run `python manage.py migrate` to create the hpc models.

4. Start the development server and visit http://127.0.0.1:8000/TBD
   to create to use it.
