view:
	open http://127.0.0.1:8000/comet/status

migrate:
	python manage.py migrate --run-syncdb

run: migrate
	python manage.py runserver

cleandb:
	rm -f db.*

initdb: cleandb
	python manage.py syncdb

doc:
	open http://127.0.0.1:8080/docs/

install:
	cd ../client; python setup.py install


######################################################################
# CLEANING
######################################################################

clean:
	# cd docs; make clean
	rm -rf build dist docs/build .eggs *.egg-info
	rm -rf *.egg-info
	find . -name "*~" -exec rm {} \;
	find . -name "*.pyc" -exec rm {} \;
	find . -name "*.db" -exec rm {} \;
	echo "clean done"
	

