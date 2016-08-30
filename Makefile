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
	cd ../client; python setup.py install
	cd ../workflow; python setup.py install


######################################################################
# CLEANING
######################################################################

clean:
	# cd docs; make clean
	rm -rf build dist docs/build .eggs *.egg-info
	rm -rf *.egg-info
	find . -name "*~" -exec rm {} \;
	find . -name "*.pyc" -exec rm {} \;
	echo "clean done"


