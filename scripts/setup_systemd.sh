#!/bin/sh -e

echo "Creating systemd unit file..."
printf "
[Unit]
Description= Oasis-Hive startup script w/ permissions & virtualenv

[Service]
ExecStart= /bin/sh /home/pi/oasis-hive/start.sh  #in this line specify the path to the script.

[Install]
WantedBy=multi-user.target
" | sudo tee /etc/systemd/system/oasis-hive.service

sudo chmod +x /home/pi/oasis-hive/start.sh
sudo systemctl enable oasis-hive
sudo systemctl start oasis-hive
sudo systemctl status oasis-hive