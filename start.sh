#!/bin/sh -e

sudo chmod -R +rwx /home/pi/oasis-hive
sudo chmod +rwx /etc/wpa_supplicant/wpa_supplicant.conf
sudo chmod +rwx /etc/network/interfaces_backup
sudo chmod +rwx /etc/network/interfaces
sudo chmod +rwx /home/pi/image.jpg
sudo chmod +rwx /etc/hostapd/hostapd.conf
sudo chmod +rwx /etc/dhcpcd.conf
sudo chmod +rwx /etc/dhcpcd_backup.conf
sudo chmod +rwx /etc/dnsmasq.conf
sudo chmod +rwx /etc/dnsmasq_backup.conf
. /home/pi/oasis-hive_venv/bin/activate
/usr/bin/env python3 /home/pi/oasis-hive/main.py