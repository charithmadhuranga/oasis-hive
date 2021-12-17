#!/bin/sh -e

sudo chmod +w /etc/rc.local
sudo sed -ie "/^fi/a v4l2-ctl --set-ctrl=rotate=90" /etc/rc.local
sudo sed -ie "/^fi/a python3 /home/pi/oasis-hive/main.py &" /etc/rc.local
sudo sed -ie "/^fi/a source /home/pi/oasis-hive_venv/bin/activate" /etc/rc.local
sudo sed -ie "/^fi/a sudo chmod -R +rwx /home/pi/oasis-hive" /etc/rc.local