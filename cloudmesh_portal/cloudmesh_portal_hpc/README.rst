Cloudmesh HPC
=============

Cloudmesh HPC allows you to add high performance queuing systems of supercomputers to your django applications,

Detailed documentation will bi in the "docs" directory.

Quick start
-----------

1. Add "cloudmesh hpc" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'cloudmesh_portal_hpc',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^hpc/', include('hpc.urls')),


3. Make sure you include the HPC queues you like to work with in the
   ~/.cloudmesh/cloudmesh.yaml file. Please see the "cloudmesh client"
   documentation in github:

   * http://cloudmesh.github.io/client/
   
3. Run `python manage.py migrate` to create the hpc models.

4. Start the development server and visit http://127.0.0.1:8000/hpc
   to create to use it.
