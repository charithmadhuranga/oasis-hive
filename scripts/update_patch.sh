#/bin/sh -e

echo "Running shell commands to update system environment..."
source /home/pi/oasis-hive/scripts/setup_config.sh
source /home/pi/oasis-hive/scripts/optimize_boot.sh -no_bt

