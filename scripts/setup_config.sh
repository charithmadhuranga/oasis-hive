#!/bin/sh -e

echo "Creating local directories..."
mkdir /home/pi/oasis-hive/configs
mkdir /home/pi/oasis-hive/data_out
mkdir /home/pi/oasis-hive/data_out/image_feed
mkdir /home/pi/oasis-hive/data_out/sensor_feed

echo "Moving configuration files..."
cp /home/pi/oasis-hive/defaults/hardware_config_default_template.json /home/pi/oasis-hive/configs/hardware_config.json
cp /home/pi/oasis-hive/defaults/access_config_default_template.json /home/pi/oasis-hive/configs/access_config.json
cp /home/pi/oasis-hive/defaults/feature_toggles_default_template.json /home/pi/oasis-hive/configs/feature_toggles.json
cp /home/pi/oasis-hive/defaults/device_state_default_template.json /home/pi/oasis-hive/configs/device_state.json
cp /home/pi/oasis-hive/defaults/hive_params_default_template.json /home/pi/oasis-hive/configs/hive_params.json

echo "Creating new lock_file..."
cp /home/pi/oasis-hive/defaults/locks_default_template.json /home/pi/oasis-hive/configs/locks.json

echo "Creating placeholder image..."
cp /home/pi/oasis-hive/defaults/default_placeholder_image.jpg /home/pi/image.jpg
