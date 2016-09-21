view:
	open http://127.0.0.1:8000

migrate:
	cd cloudmesh_portal; python manage.py migrate

run: migrate
	cd cloudmesh_portal; python manage.py runserver

cleandb:
	rm -f db.*

initdb: cleandb
	cd cloudmesh_portal; python manage.py syncdb

doc:
	open http://127.0.0.1:8000

install:
	# cd ../client; python setup.py install
	# cd ../workflow; python setup.py install
	make -f Makefile sdist
	make -f Makefile deploy

sdist:
	cd cloudmesh_portal/cloudmesh_portal_hpc; python setup.py sdist
	cd cloudmesh_portal/cloudmesh_portal_comet; python setup.py sdist

deploy: sdist
	pip install cloudmesh_portal/cloudmesh_portal_hpc/dist/django-cloudmesh-portal-hpc-*.tar.gz
	pip install cloudmesh_portal/cloudmesh_portal_hpc/dist/django-cloudmesh-portal-comet-*.tar.gz


uninstall:
	pip uninstall django-cloudmesh-portal-hpc
	pip uninstall django-cloudmesh-portal-comet

######################################################################
# CLEANING
######################################################################

clean:
	# cd docs; make clean
	rm -rf build dist docs/build .eggs *.egg-info
	rm -rf *.egg-info
	find . -name "dist" -exec rm -rf {} \;
	find . -name "*~" -exec rm {} \;
	find . -name "*.pyc" -exec rm {} \;
	echo "clean done"


