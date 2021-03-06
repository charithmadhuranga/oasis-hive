#system
import os
import os.path
import sys

#set proper path for modules
sys.path.append('/home/pi/oasis-hive')
sys.path.append('/home/pi/oasis-hive/utils')
sys.path.append('/usr/lib/python37.zip')
sys.path.append('/usr/lib/python3.7')
sys.path.append('/usr/lib/python3.7/lib-dynload')
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
sys.path.append('/usr/local/lib/python3.7/dist-packages')
sys.path.append('/usr/lib/python3/dist-packages')

#Process management
import serial
import subprocess
from subprocess import Popen, PIPE, STDOUT
import signal
import gc
import traceback

#communicating with firebase
import requests

#data handling
import json
import csv
from csv import writer

#dealing with specific times of the day
import time
import datetime

#import other oasis packages
import reset_model

#declare process management variables
ser_in = None
sensor_info = None
heat_process = None
dehumidify_process = None
camera_process = None

#declare sensor data variables
temperature = 0
humidity = 0
last_temperature = 0
last_humidity = 0
last_target_temperature = 0
last_target_humidity = 0

#declare timekeeping variables
data_timer = None
sensor_log_timer = None

#declare state variables
#these should never be modified from within python, only loaded with load_state()
#use write_state() to change a value 
device_state = None #describes the current state of the system
hive_params = None #describes the grow configuration of the system
hardware_config = None #holds hardware I/O setting & pin #s
access_config = None #contains credentials for connecting to firebase
feature_toggles = None #tells the system which features are in use

#declare locking variables
locks = None

def load_state(loop_limit=100000): #Depends on: 'json'; Modifies: device_state,hardware_config ,access_config
    global device_state, hive_params, access_config, feature_toggles, hardware_config

    #load device state
    for i in list(range(int(loop_limit))): #try to load, check if available, make unavailable if so, write state if so, write availabke iff so,  
        try:
            with open("/home/pi/oasis-hive/configs/device_state.json") as d:
                device_state = json.load(d) #get device state

            for k,v in device_state.items(): 
                if device_state[k] is None:
                    print("Read NoneType in device_state")
                    print("Resetting device_state...") 
                    reset_model.reset_device_state()
                else: 
                    pass    
        
            break
            
        except Exception as e:
            if i == int(loop_limit):
                reset_model.reset_device_state()
                print("Main.py tried to read max # of times. File is corrupted. Resetting device state ...")
            else:
                print("Main.py tried to read while file was being written. If this continues, file is corrupted.")
                pass
    
    #load hive_params
    for i in list(range(int(loop_limit))): #try to load, check if available, make unavailable if so, write state if so, write availabke iff so,  
        try:
            with open("/home/pi/oasis-hive/configs/hive_params.json") as g:
                hive_params = json.load(g) #get device state

            for k,v in hive_params.items(): 
                if hive_params[k] is None:
                    print("Read NoneType in hive_params")
                    print("Resetting hive_params...")
                    reset_model.reset_hive_params()
                     
                else: 
                    pass    
        
            break
            
        except Exception as e:
            if i == int(loop_limit):
                print("Main.py tried to read max # of times. File is corrupted. Resetting hive_params...")
                reset_model.reset_hive_params()
            else:
                print("Main.py tried to read while hive_params was being written. If this continues, file is corrupted.")
                pass   

    #load access_config
    for i in list(range(int(loop_limit))): #try to load, check if available, make unavailable if so, write state if so, write availabke iff so,  
        try:
            with open("/home/pi/oasis-hive/configs/access_config.json") as a:
                access_config = json.load(a) #get device state

            for k,v in access_config.items(): 
                if access_config[k] is None:
                    print("Read NoneType in access_config")
                    print("Resetting access_config...")
                    reset_model.reset_access_config()
                     
                else: 
                    pass    
        
            break
            
        except Exception as e:
            if i == int(loop_limit):
                print("Main.py tried to read max # of times. File is corrupted. Resetting access_config...")
                reset_model.reset_access_config()
            else:
                print("Main.py tried to read while access_config was being written. If this continues, file is corrupted.")
                pass               

    #load feature_toggles
    for i in list(range(int(loop_limit))): #try to load, check if available, make unavailable if so, write state if so, write availabke iff so,  
        try:
            with open("/home/pi/oasis-hive/configs/feature_toggles.json") as f:
                feature_toggles = json.load(f) #get device state

            for k,v in feature_toggles.items(): 
                if feature_toggles[k] is None:
                    print("Read NoneType in feature_toggles")
                    print("Resetting feature_toggles...")
                    reset_model.reset_feature_toggles()
                     
                else: 
                    pass    
        
            break
            
        except Exception as e:
            if i == int(loop_limit):
                print("Main.py tried to read max # of times. File is corrupted. Resetting feature_toggles...")
                reset_model.reset_feature_toggles()
            else:
                print("Main.py tried to read while feature_toggles was being written. If this continues, file is corrupted.")
                pass
            
    #load hardware_config
    for i in list(range(int(loop_limit))): #try to load, check if available, make unavailable if so, write state if so, write availabke iff so,  
        try:
            with open("/home/pi/oasis-hive/configs/hardware_config.json") as h:
                hardware_config = json.load(h) #get device state

            for k,v in hardware_config.items(): 
                if hardware_config[k] is None:
                    print("Read NoneType in hardware_config")
                    print("Resetting hardware_config...")
                    reset_model.reset_hardware_config()
                     
                else: 
                    pass    
        
            break
            
        except Exception as e:
            if i == int(loop_limit):
                print("Main.py tried to read max # of times. File is corrupted. Resetting hardware_config...")
                reset_model.reset_hardware_config()
            else:
                print("Main.py tried to read while hardware_config was being written. If this continues, file is corrupted.")
                pass
            
#modifies a firebase variable
def patch_firebase(field,value): #Depends on: load_state(),'requests','json'; Modifies: database['field'], state variables
    load_state()
    data = json.dumps({field: value})
    url = "https://oasis-1757f.firebaseio.com/"+str(access_config["local_id"])+"/"+str(access_config["device_name"])+".json?auth="+str(access_config["id_token"])
    result = requests.patch(url,data)

def load_locks(loop_limit = 10000):
    global locks
    for i in list(range(int(loop_limit))): #try to load, check if available, make unavailable if so, write state if so, write availabke iff so,  
        try:
            with open("/home/pi/oasis-hive/configs/locks.json","r+") as l:
                locks = json.load(l) #get locks

            for k,v in locks.items():
                if locks[k] is None:
                    print("Read NoneType in locks")
                    print("Resetting locks...")
                    reset_model.reset_locks()  
                else: 
                    pass
             
            break   
    
        except Exception as e:
            if i == int(loop_limit):
                print("Tried to load lock max number of times. File is corrupted. Resetting locks...")
                reset_model.reset_locks()
            else:
                print("Main.py tried to read while locks were being written. If this continues, file is corrupted.")
                pass

def lock(file):
    global locks
    
    with open("/home/pi/oasis-hive/configs/locks.json", "r+") as l:
        locks = json.load(l) #get lock
        
        if file == "device_state":
            locks["device_state_write_available"] = "0" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
                
        if file == "hive_params":
            locks["hive_params_write_available"] = "0" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
            
        if file == "access_config":
            locks["access_config_write_available"] = "0" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
    
        if file == "feature_toggles":
            locks["feature_toggles_write_available"] = "0" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
        
        if file == "hardware_config":
            locks["hardware_config_write_available"] = "0" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()

def unlock(file):
    global locks
    
    with open("/home/pi/oasis-hive/configs/locks.json", "r+") as l:
        locks = json.load(l) #get lock
        
        if file == "device_state":
            locks["device_state_write_available"] = "1" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
                
        if file == "hive_params":
            locks["hive_params_write_available"] = "1" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
            
        if file == "access_config":
            locks["access_config_write_available"] = "1" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
    
        if file == "feature_toggles":
            locks["feature_toggles_write_available"] = "1" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
        
        if file == "hardware_config":
            locks["hardware_config_write_available"] = "1" #let system know resource is not available
            l.seek(0)
            json.dump(locks, l)
            l.truncate()
            
#save key values to .json
def write_state(path,field,value,loop_limit=100000): #Depends on: load_state(), patch_firebase, 'json'; Modifies: path
    
    #these will be loaded in by the listener, so best to make sure we represent the change in firebase too
    if device_state["connected"] == "1": #write state to cloud
        try:
            patch_firebase(field,value)
        except Exception as e:
            print(e)
            pass
  
    for i in list(range(int(loop_limit))): #try to load, check if available, make unavailable if so, write state if so, write availabke iff so, 
        
        load_locks()
        
        try:
            with open(path, "r+") as x: # open the file.
                data = json.load(x) # can we load a valid json?

                if path == "/home/pi/oasis-hive/configs/device_state.json": #are we working in device_state?
                    if locks["device_state_write_available"] == "1": #check is the file is available to be written
                        lock("device_state")

                        data[field] = value #write the desired value
                        x.seek(0)
                        json.dump(data, x)
                        x.truncate()

                        unlock("device_state")
                        
                        load_state()
                        break #break the loop when the write has been successful

                    else:
                        pass
                    
                if path == "/home/pi/oasis-hive/configs/hive_params.json": #are we working in device_state?
                    if locks["hive_params_write_available"] == "1": #check is the file is available to be written
                        lock("hive_params")

                        data[field] = value #write the desired value
                        x.seek(0)
                        json.dump(data, x)
                        x.truncate()
            
                        unlock("hive_params")
                        
                        load_state()
                        break #break the loop when the write has been successful

                    else:
                        pass
                    
                if path == "/home/pi/oasis-hive/configs/access_config.json": #are we working in device_state?
                    if locks["access_config_write_available"] == "1": #check is the file is available to be written
                        lock("access_config")

                        data[field] = value #write the desired value
                        x.seek(0)
                        json.dump(data, x)
                        x.truncate()

                        unlock("access_config")
                        
                        load_state()
                        break #break the loop when the write has been successful

                    else:
                        pass
                    
                if path == "/home/pi/oasis-hive/configs/feature_toggles.json": #are we working in device_state?
                    if locks["feature_toggles_write_available"] == "1": #check is the file is available to be written
                        lock("feature_toggles")

                        data[field] = value #write the desired value
                        x.seek(0)
                        json.dump(data, x)
                        x.truncate()

                        unlock("feature_toggles")
                        
                        load_state()
                        break #break the loop when the write has been successful

                    else:
                        pass
                    
                if path == "/home/pi/oasis-hive/configs/hardware_config.json": #are we working in device_state?
                    if locks["hardware_config_write_available"] == "1": #check is the file is available to be written
                        lock("hardware_config")

                        data[field] = value #write the desired value
                        x.seek(0)
                        json.dump(data, x)
                        x.truncate()

                        unlock("hardware_config")
                        
                        load_state()
                        break #break the loop when the write has been successful

                    else:
                        pass

        except Exception as e: #If any of the above fails:
            if i == int(loop_limit):
                print("Tried to write state multiple times. File is corrupted. Resetting locks...")
                reset_model.reset_locks()
            else:
                print(e)
                print("Could not load locks. If this error persists, the lock file is corrupted. Retrying...")
                pass #continue the loop until write is successful or ceiling is hit

#write some data to a .csv, takes a dictionary and a path
def write_csv(filename, dict): 
    file_exists = os.path.isfile(filename)

    with open (filename, 'a') as csvfile:
        headers = ["time", "temperature", "humidity"]
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=headers)

        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header

        writer.writerow(dict)
    
    return 

#attempts connection to microcontroller
def start_serial(): #Depends on:'serial'; Modifies: ser_out
    global ser_in

    try:
        try:
            ser_in = serial.Serial("/dev/ttyUSB0", 9600)
            print("Started serial communication with Arduino Nano.")
        except:
            ser_in = serial.Serial("/dev/ttyACM0", 9600)
            print("Started serial communication with Arduino Uno.")
    except Exception as e:
        #ser_in = None
        print("Serial connection not found")

#gets data from serial THIS WILL HAVE TO BE DEPRECATED SOON IN FAVOR OF AN ON-BOARD SENSOR SUITE
def listen(): #Depends on 'serial', start_serial(); Modifies: ser_in, sensor_info, temperature, humidity, last_temperature, last_humidity
    #load in global vars
    global ser_in,sensor_info,temperature,humidity,last_temperature,last_humidity

    if ser_in == None:
        return

    #listen for data from aurdino
    sensor_info = ser_in.readline().decode('UTF-8').strip().split(' ')

    if len(sensor_info)<2:
        pass
    else:
        #print and save our data
        last_humidity = humidity
        humidity =float(sensor_info[0])

        last_temperature = temperature
        temperature =float(sensor_info[1])

#PD controller to modulate heater feedback
def heat_pd(temperature, target_temperature, last_temperature, last_target_temperature, P_heat, D_heat): #no dependencies

    err_temperature = target_temperature-temperature    #If target is 70 and temperature is 60, this value = 10, more heat
                                                        #If target is 50 and temperature is 60, this value is negative, less heat

    temperature_dot = temperature-last_temperature  #If temp is increasing, this value is positive (+#)
                                                    #If temp is decreasing, this value is negative (-#)

    target_temperature_dot = target_temperature-last_target_temperature #When target remains the same, this value is 0
                                                                        #When adjusting target up, this value is positive (+#)
                                                                        #When adjusting target down, this value is negative (-#)

    err_dot_temperature = target_temperature_dot-temperature_dot    #When positive, boosts heat signal
                                                                    #When negative, dampens heat signal
    heat_level  = P_heat * err_temperature + D_heat * err_dot_temperature
    heat_level  = max(min(int(heat_level), 100), 0)

    return heat_level

#PD controller to modulate dehumidifier feedback
def dehum_pd(humidity, target_humidity, last_humidity, last_target_humidity, P_hum, D_hum): #no dependencies

    err_humidity = humidity - target_humidity   #If target is 60 and humidity is 30, this value is negative, less dehum
                                                #If target is 30 and humidity is 60, this value = 30, more dehum
 
    humidity_dot = last_humidity - humidity #If hum increasing, this value is negative (-#)
                                            #If hum decreasing, this value is positive (+#)

    target_humidity_dot = last_target_humidity - target_humidity    #When target remains the same, this value is 0
                                                                    #When adjusting target down, this value is positive (+#)
                                                                    #When adjusting target up, this value is negative (-#)

    err_dot_humidity = humidity_dot - target_humidity_dot   #When positive, dampens dehum signal
                                                            #When negative, boosts duhum signal

    dehumidify_level  = P_hum * err_humidity + D_hum * (0 - err_dot_humidity)
    dehumidify_level  = max(min(int(dehumidify_level), 100), 0)

    return dehumidify_level

#poll heat subprocess if applicable and relaunch/update actuators
def run_heat(intensity): #Depends on: 'subprocess'; Modifies: heat_process
    global heat_process

    try:
        poll_heat = heat_process.poll() #heat
        if poll_heat is not None:
            heat_process = Popen(['python3', '/home/pi/oasis-hive/actuators/heatingElement.py', str(intensity)]) #If running, then skips. If idle then restarts, If no process, then fails
    except:
        heat_process = Popen(['python3', '/home/pi/oasis-hive/actuators/heatingElement.py', str(intensity)]) #If no process, then starts

#poll dehumidify subprocess if applicable and relaunch/update actuators
def run_hum(intensity): #Depends on: 'subprocess'; Modifies: hum_process
    global dehumidify_process

    try:
        poll_dehumidify = dehumidify_process.poll() #dehumidify
        if poll_dehumidify is not None:
            dehumidify_process = Popen(['python3', '/home/pi/oasis-hive/actuators/dehumidifyElement.py', str(intensity)]) #If running, then skips. If idle then restarts, If no process, then fails
    except:
        dehumidify_process = Popen(['python3', '/home/pi/oasis-hive/actuators/dehumidifyElement.py', str(intensity)]) #If no process, then starts

#poll camera subprocess if applicable and relaunch/update actuators
def run_camera(picture_frequency): #Depends on: 'subprocess'; Modifies: camera_process
    global camera_process

    try:
        poll_camera = camera_process.poll() #camera
        if poll_camera is not None:
            camera_process = Popen(['python3', '/home/pi/oasis-hive/imaging/cameraElement.py', str(picture_frequency)]) #If running, then skips. If idle then restarts, If no process, then fails
    except:
        camera_process = Popen(['python3', '/home/pi/oasis-hive/imaging/cameraElement.py', str(picture_frequency)]) #If no process, then starts

def clean_up_processes():
    global heat_process, dehumidify_process, camera_process       

    #clean up all processes
    load_state()

    if (feature_toggles["heater"] == "1") and (heat_process != None): #go through toggles and kill active processes
        heat_process.terminate()
        heat_process.wait()

    if (feature_toggles["dehumidifier"] == "1") and (dehumidify_process != None):
        dehumidify_process.terminate()
        dehumidify_process.wait()

    if (feature_toggles["camera"] == "1") and (camera_process != None):
        camera_process.terminate()
        camera_process.wait()

    gc.collect()

#terminates the program and all running subprocesses
def terminate_program(): #Depends on: load_state(), 'sys', 'subprocess' #Modifies: heat_process, dehumidify_process,  camera_process

    print("Terminating Program...")
    clean_up_processes()

    #flip "running" to 0
    write_state("/home/pi/oasis-hive/configs/device_state.json", "running", "0")

    sys.exit()

def main_setup():
    global data_timer, sensor_log_timer

    #Load state variables to start the main program
    load_state()

    #Exit early if opening subprocess daemon
    if str(sys.argv[1]) == "daemon":
        print("hive_ctrl daemon started")
        #kill the program
        sys.exit()
    if str(sys.argv[1]) == "main":
        print("hive_ctrl main started")
        #flip "running" to 1 to make usable from command line
        write_state("/home/pi/oasis-hive/configs/device_state.json", "running", "1")
        #continue with program execution
        pass
    else:
        print("please offer valid run parameters")
        sys.exit()

    #attempt to make serial connection
    start_serial()

    #start the clock for timimg .csv writes and data exchanges with server
    data_timer = time.time()
    sensor_log_timer = time.time()

def main_loop():
    global data_timer, sensor_log_timer, last_target_temperature, last_target_humidity, device_state

    #launch main program loop
    try:
        print("------------------------------------------------------------")

        while True:

            last_target_temperature = int(hive_params["target_temperature"]) #save last temperature and humidity targets to calculate delta for PD controllers
            last_target_humidity = int(hive_params["target_humidity"])

            load_state() #regresh the state variables to get new parameters


            if (feature_toggles["temp_hum_sensor"] == "1"):
                try: #attempt to read data from sensor, raise exception if there is a problem
                    listen() #this will be changed to run many sensor functions as opposed to one serial listener
                except Exception as e:
                    print(e)
                    print("Serial Port Failure")

            if feature_toggles["heater"] == "1":
                print("Target Temperature: %.1f F | Current: %.1f F | Temp_PID: %s %%"%(int(hive_params["target_temperature"]),temperature, heat_pd(temperature,
                                                                                                                                  int(hive_params["target_temperature"]),
                                                                                                                                  last_temperature,
                                                                                                                                  last_target_temperature,
                                                                                                                                  int(hive_params["P_temp"]),
                                                                                                                                  int(hive_params["D_temp"]))))
            if feature_toggles["dehumidifier"] == "1":
                print("Target Humidity: %.1f %% | Current: %.1f %% | DeHum_PID: %s %%"%(int(hive_params["target_humidity"]), humidity, dehum_pd(humidity,
                                                                                                                               int(hive_params["target_humidity"]),
                                                                                                                               last_humidity,
                                                                                                                               last_target_humidity,
                                                                                                                               int(hive_params["P_hum"]),
                                                                                                                               int(hive_params["D_hum"]))))

            if feature_toggles["camera"] == "1":
                print("Image every %i minute(s)"%(int(hive_params["camera_interval"])))



            print("------------------------------------------------------------")

            #write data and send to server after set time elapses
            if time.time() - data_timer > 300:

                try:

                    if feature_toggles["save_data"] == "1":
                        #save data to .csv
                        print("Writing to csv")
                        write_csv('/home/pi/oasis-hive/data_out/sensor_feed/sensor_data.csv',{"time": [str(time.strftime('%l:%M%p %Z %b %d, %Y'))], "temperature": [str(temperature)], "humidity": [str(humidity)]})

                    write_state("/home/pi/oasis-hive/configs/device_state.json", "temperature", str(temperature))
                    write_state("/home/pi/oasis-hive/configs/device_state.json", "humidity", str(humidity))

                    data_timer = time.time()

                except Exception as e:
                    print(e)
                    data_timer = time.time()

            #update actuators in use
            if feature_toggles["heater"] == "1":
                run_heat(str(heat_pd(temperature,int(hive_params["target_temperature"]),last_temperature,last_target_temperature,int(hive_params["P_temp"]),int(hive_params["D_temp"]))))
            if feature_toggles["dehumidifier"] == "1":
                run_hum(str(dehum_pd(humidity,int(hive_params["target_humidity"]),last_humidity,last_target_humidity,int(hive_params["P_hum"]),int(hive_params["D_hum"]))))
            if feature_toggles["camera"] == "1":
                run_camera(int(hive_params["camera_interval"]))
    

            #set exit condition
            load_state()
            if device_state["running"] == "0":
                terminate_program()
            else:
                pass

            #give the program some time to breathe
            time.sleep(1)

    except (KeyboardInterrupt):
        terminate_program()

    except Exception as e:
        traceback.print_exc()
        if device_state["running"] == "1": #if there is an error, but device should stay running
            clean_up_processes()
        if device_state["running"] == "0":
            terminate_program()
            
if __name__ == '__main__':
    main_setup()
    main_loop()

