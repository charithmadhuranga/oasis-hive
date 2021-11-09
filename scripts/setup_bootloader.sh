#!/bin/sh -e

sudo chmod +w /etc/rc.local
sudo sed -ie "/^fi/a v4l2-ctl --set-ctrl=rotate=90" /etc/rc.local
sudo sed -ie "/^fi/a sudo python3 /home/pi/oasis-hive/main.py &" /etc/rc.local