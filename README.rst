Install
--------
mkdir -p ~/github/cloudmesh

cd ~/github/cloudmesh
git clone https://github.com/cloudmesh/client.git
cd client
pip install -r requirements.txt
python setup.py install

cd ~/github/cloudmesh

git clone https://github.com/cloudmesh/portal.git
cd portal
pip install -r requirements.txt
python setup.py install


Run portal
-----------

make run

View portal 
-------------

Make view
