import nidaqmx as ni
#from .log import csv_write
from datetime import datetime
import time


#valve info dump for LE
#ch0 --> LOX Release Mechanism(LRM): closed, but also unused for LE
#ch1 --> Helium Release Mechanism: closed(HRM), null state
#ch2 --> MPVA OX(Main Propellant Valve Actuator, OX): closed
#ch3 --> MPVA Fuel (Main Propellant Valve Actuator, Fuel): closed
#ch4 --> OB PNU (Onboard Pneumatics): open
#ch5 --> HE Vent(Helium Vent): open
#ch6 --> HE Prime: closed
#ch7 --> HE Fill: closed
#ch8 --> igniter continuity and ignition(?)

def open_nc_valve(task):# , name, queue, csv_file_path):
    #supplies power to normally closed valve to open it
    task.write([True], auto_start=True)
    
    # queue.put('open')

    # timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    # out = [timestamp, name, 'open']
    # csv_write(out, csv_file_path)

def close_nc_valve(task):#, name, queue, csv_file_path):
    #removes power to normally closed valve to close it
    task.write([False], auto_start=True)

    # queue.put('closed')

    # timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    # out = [timestamp, name, 'closed']
    # csv_write(out, csv_file_path)

def open_no_valve(task):#, name, queue, csv_file_path):
    #removes power to normally open valve to open it
    task.write([False], auto_start=True)

    # queue.put('open')

    # timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    # out = [timestamp, name, 'open']
    # csv_write(out, csv_file_path)

def close_no_valve(task): #, name, queue, csv_file_path):
    # supplies power to normally open valve to close it
    task.write([True], auto_start=True)

    # queue.put('closed')

    # timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    # out = [timestamp, name, 'closed']
    # csv_write(out, csv_file_path)

def chann_disable(task):
    #does not allow change on channel
    task.do_tristate(task, True)
    

def chann_enable(task):
    #allows change on channel
    task.do_tristate(task, False)

def ignite(task):
    task.write([True], auto_start=True)
    time.sleep(3)
    task.write([False], auto_start=True)
