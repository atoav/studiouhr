# Instuctions

## Raspbian

Configure sleep settings `sudo nano /etc/lightdm/lightdm.conf`

Find the line after [Seat:*] and change it to `xserver-command=X -s 0 -dpms`

Append this to the file `sudo vim ~/.config/lxsession/LXDE-pi/autostart`

```sh
@xset s noblank                 #don't blank the video device
@xset s off                     #disable screen saver
@xset -dpms                     #disable DPMS power management features (sleep)
@unclutter -idle 0.1 -root      #hide pointer when mouse idle for more than X seconds

# Start Studiouhr
@sh /home/pi/start_studiouhr.sh
```



Activate the built-in *systemd* software/hardware *watchdog* service to automatically reboot the Pi if hung

`sudo vim /etc/systemd/system.conf` uncomment:

```sh
#RuntimeWatchdogSec=0
#ShutdownWatchdogSec=10min

to

RuntimeWatchdogSec=10
ShutdownWatchdogSec=10min
```

Add a 

## Set Timeserver

```
/etc/ntp.conf
```

```
# Check Timeserver
ntpq -p
```

## Autostart Studiouhr

Autostart for studiouhr script is located in `/etc/xdg/lxsession/LXDE/autostart`

For a start from ssh run `export DISPLAY=:0` before

## Update

To load the recent version from the github repo, go to the studiouhr folder `cd /home/pi/studiouhr/` and pull from the remote repository with `git pull origin master`

#### update.sh

```sh
git fetch --all
git reset --hard origin/master
source .env/bin/activate
pip install --upgrade .
```



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

#### install.sh

```sh
sudo pip install virtualenv
virtualenv .env
source .env/bin/activate
pip install .
cd /usr/local/bin
sudo ln -s ~/studiouhr/.env/bin/studiouhr
cd -
source .env/bin/activate
pip install --upgrade .
```

