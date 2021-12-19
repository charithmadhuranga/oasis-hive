#!/bin/sh -e

sudo chmod +w /etc/rc.local
sudo sed -ie "/^fi/a v4l2-ctl --set-ctrl=rotate=90" /etc/rc.local
sudo sed -ie "/^fi/a /usr/bin/env python3 /home/pi/oasis-hive/main.py &" /etc/rc.local
sudo sed -ie "/^fi/a . /home/pi/oasis-hive_venv/bin/activate" /etc/rc.local
sudo sed -ie "/^fi/a sudo chmod +rwx /home/pi/image.jpg" /etc/rc.local
sudo sed -ie "/^fi/a sudo chmod +rwx /etc/hostapd/hostapd.conf" /etc/rc.local
sudo sed -ie "/^fi/a sudo chmod +rwx /etc/dhcpcd.conf" /etc/rc.local
sudo sed -ie "/^fi/a sudo chmod +rwx /etc/dhcpcd_backup.conf" /etc/rc.local
sudo sed -ie "/^fi/a sudo chmod +rwx /etc/dnsmasq.conf" /etc/rc.local
sudo sed -ie "/^fi/a sudo chmod +rwx /etc/dnsmasq_backup.conf" /etc/rc.local
sudo sed -ie "/^fi/a sudo chmod +rwx /etc/network/interfaces" /etc/rc.local
sudo sed -ie "/^fi/a sudo chmod +rwx /etc/network/interfaces_backup" /etc/rc.local
sudo sed -ie "/^fi/a sudo chmod +rwx /etc/wpa_supplicant/wpa_supplicant.conf" /etc/rc.local
sudo sed -ie "/^fi/a sudo chmod -R +rwx /home/pi/oasis-hive" /etc/rc.local