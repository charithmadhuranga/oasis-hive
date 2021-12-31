#!/bin/sh -e

sudo chmod -R +x /home/pi/oasis-hive/scripts

while getopts ":r:d" opt; do
    case $opt in
        r)
            echo "Adding rc.local bootloader..."
            . /home/pi/oasis-hive/scripts/setup_rclocal.sh
            
            echo "Optimizing boot time..."
            . /home/pi/oasis-hive/scripts/optimize_boot.sh -b        
            
            ;;
        d)
            echo "Adding systemd service..."
            . /home/pi/oasis-hive/scripts/setup_systemd.sh
            
            echo "Optimizing boot time..."
            . /home/pi/oasis-hive/scripts/optimize_boot.sh -b        
            
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