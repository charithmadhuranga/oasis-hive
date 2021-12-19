#!/bin/sh -e

sudo chmod +x /home/pi/oasis-hive/scripts/setup_env.sh
. /home/pi/oasis-hive/scripts/setup_env.sh
sudo chmod +x /home/pi/oasis-hive/scripts/setup_config.sh
. /home/pi/oasis-hive/scripts/setup_config.sh
sudo chmod +x /home/pi/oasis-hive/scripts/setup_network.sh
. /home/pi/oasis-hive/scripts/setup_network.sh

while getopts ":b" opt; do
    case $opt in
        rc_local)
            echo "Adding rc.local bootloader..."
            sudo chmod +x /home/pi/oasis-hive/scripts/setup_rclocal.sh
            . /home/pi/oasis-hive/scripts/setup_rclocal.sh
            
            echo "Optimizing boot time..."
            sudo chmod +x /home/pi/oasis-hive/scripts/optimize_boot.sh
            . /home/pi/oasis-hive/scripts/optimize_boot.sh -no_bt        
            
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            ;;
    esac
done

echo "Returning to WiFi mode..."
sudo cp /etc/dhcpcd_WiFi.conf /etc/dhcpcd.conf
sudo cp /etc/dnsmasq_WiFi.conf /etc/dnsmasq.conf
sudo systemctl disable hostapd
sudo systemctl reboot