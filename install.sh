sudo pip install virtualenv
virtualenv .env
source .env/bin/activate
pip install .
cd /usr/local/bin
sudo ln -s ~/studiouhr/.env/bin/studiouhr
cd -
source .env/bin/activate
pip install --upgrade .