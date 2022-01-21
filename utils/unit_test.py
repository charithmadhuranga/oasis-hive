from cgi import test
import os
import os.path
import sys
import subprocess
from subprocess import Popen
import json
import requests
import time

#set proper path for modules
sys.path.append('/home/pi/oasis-hive')
sys.path.append('/home/pi/oasis-hive/core')
sys.path.append('/home/pi/oasis-hive/utils')
sys.path.append('/home/pi/oasis-hive/imaging')
sys.path.append('/home/pi/oasis-hive/networking')
sys.path.append('/home/pi/oasis-hive/actuators')
sys.path.append('/usr/lib/python37.zip')
sys.path.append('/usr/lib/python3.7')
sys.path.append('/usr/lib/python3.7/lib-dynload')
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
sys.path.append('/usr/local/lib/python3.7/dist-packages')
sys.path.append('/usr/lib/python3/dist-packages')

import main
import hive_ctrl
import detect_db_events, oasis_setup
import cameraElement
import update, reset_model, send_image_test

def test_state_handlers():
    
    main.load_state()
    main.write_state("/home/pi/oasis-hive/configs/device_state.json", "running", str("1"))
    main.write_state("/home/pi/oasis-hive/configs/device_state.json", "running", str("0"))

    hive_ctrl.load_state()
    hive_ctrl.write_state("/home/pi/oasis-hive/configs/device_state.json", "running", str("1"))
    hive_ctrl.write_state("/home/pi/oasis-hive/configs/device_state.json", "running", str("0"))

    detect_db_events.load_state()
    detect_db_events.write_state("/home/pi/oasis-hive/configs/device_state.json", "running", str("1"))
    detect_db_events.write_state("/home/pi/oasis-hive/configs/device_state.json", "running", str("0"))

    oasis_setup.load_state()
    oasis_setup.write_state("/home/pi/oasis-hive/configs/device_state.json", "running", str("1"))
    oasis_setup.write_state("/home/pi/oasis-hive/configs/device_state.json", "running", str("0"))

    cameraElement.load_state()
    cameraElement.write_state("/home/pi/oasis-hive/configs/device_state.json", "running", str("1"))
    cameraElement.write_state("/home/pi/oasis-hive/configs/device_state.json", "running", str("0"))

    update.load_state()
    update.write_state("/home/pi/oasis-hive/configs/device_state.json", "running", str("1"))
    update.write_state("/home/pi/oasis-hive/configs/device_state.json", "running", str("0"))

def test_reset_model():
    reset_model.reset_device_state()
    reset_model.reset_hive_params()
    reset_model.reset_locks()

def test_serial_connections():
    main.start_serial()
    hive_ctrl.start_serial()

def test_listen():
    hive_ctrl.listen()

def test_camera():
    hive_ctrl.run_camera(0)

def test_heater():
    hive_ctrl.run_heat(10)

def test_dehumidifier():
    hive_ctrl.run_hum(10)

def test_save_csv():
    tod = str(time.strftime('%l:%M%p %Z %b %d, %Y'))
    temperature = str(70)
    humidity = str(50)
    water_low = str(0)
    hive_ctrl.write_csv('/home/pi/oasis-hive/data_out/sensor_feed/sensor_data.csv', {"time": tod, "temperature": temperature, "humidity": humidity, "water_low": water_low})

def test_cloud_connection():
    main.connect_firebase()

def test_send_image():
    send_image_test.send_image_test()

def test_update():
    update.get_update_test()

def test_install():
    validator = Popen([".", "/home/pi/oasis-hive/scripts/validate_install.sh"])
    output, error = validator.communicate()

def test_AP_up():
    main.enable_AP()

def test_WiFi_setup():
    main.check_AP()

def test_AP_down():
    main.enable_WiFi()

def test_all_components():
    test_install()
    test_state_handlers()
    test_reset_model()
    test_serial_connections()
    test_listen()
    test_camera()
    test_heater()
    test_dehumidifier()
    test_save_csv()
    test_cloud_connection()
    test_send_image()
    test_update()
    

if __name__ == "__main__":
   test_all_components()
