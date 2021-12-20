#!/bin/sh -e

sudo chmod +w /etc/rc.local
sudo sed -ie "/^fi/a . /home/pi/oasis-hive/start.sh &" /etc/rc.local