# Instuctions

## Autostart Studiouhr

Autostart for studiouhr script is located in `/etc/xdg/lxsession/LXDE/autostart`

For a start from ssh run `export DISPLAY=:0` before

## Update

To load the recent version from the github repo, go to the studiouhr folder `cd /home/pi/studiouhr/` and pull from the remote repository with `git pull origin master`



## Setup Virtualenv

Make sure virtualenv is installed `pip install virtualenv`

Enter your projects directory and setup a new virtualenv. Start the virtualenv and install a studiouhr with pip

```
virtualenv .env
source .env/bin/activate
pip install .
```



Make a symlink to the bin within the virtualenv

```
cd /usr/local/bin
sudo ln -s ~/studiouhr/.env/bin/studiouhr
```

If you want to update the script:

```
cd ~/studiouhr
source .env/bin/activate
pip install --upgrade .
```

