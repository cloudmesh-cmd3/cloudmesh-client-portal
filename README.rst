Install
--------
mkdir -p ~/github/cloudmesh

cd ~/github/cloudmesh
git clone https://github.com/cloudmesh/client.git
cd client
pip install -r requirements.txt
python setup.py install

cd ~/github/cloudmesh


cd ~/github/cloudmesh
git clone https://github.com/cloudmesh/workflow.git
cd workflow
pip install -r requirements.txt
pip install .

cd ~/github/cloudmesh

git clone https://github.com/cloudmesh/portal.git
cd portal
pip install -r requirements.txt
python setup.py install
make admin
make run


Add Admin
----------

make admin

open http://127.0.0.1:8000/admin/


Run portal
-----------

make run

View portal 
-------------

make view

Todo
-------------


cm portal user add ... --admin
cm portal user delete

cm portal group add
cm portal group activate
cm portal group deactivate

we need groups

admin   - a user that is an admin of the portal
user    - a user able to use the portal
applied - a user that just has applied

how do we save a group that was created with gui so we can reimport



