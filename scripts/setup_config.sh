#!/bin/sh -e

echo "Creating local directories..."
sudo mkdir /home/pi/oasis-hive/configs
sudo mkdir /home/pi/oasis-hive/data_out
sudo mkdir /home/pi/oasis-hive/data_out/image_feed
sudo mkdir /home/pi/oasis-hive/data_out/sensor_feed

echo "Moving configuration files..."
sudo cp /home/pi/oasis-hive/defaults/hardware_config_default_template.json /home/pi/oasis-hive/configs/hardware_config.json
sudo cp /home/pi/oasis-hive/defaults/access_config_default_template.json /home/pi/oasis-hive/configs/access_config.json
sudo cp /home/pi/oasis-hive/defaults/feature_toggles_default_template.json /home/pi/oasis-hive/configs/feature_toggles.json
sudo cp /home/pi/oasis-hive/defaults/device_state_default_template.json /home/pi/oasis-hive/configs/device_state.json
sudo cp /home/pi/oasis-hive/defaults/hive_params_default_template.json /home/pi/oasis-hive/configs/hive_params.json

echo "Creating new lock_file..."
sudo cp /home/pi/oasis-hive/defaults/locks_default_template.json /home/pi/oasis-hive/configs/locks.json

echo "Creating placeholder image..."
sudo cp /home/pi/oasis-hive/defaults/default_placeholder_image.jpg /home/pi/image.jpg
