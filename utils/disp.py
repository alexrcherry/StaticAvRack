import tkinter as tk
from tkinter import messagebox, Button, Label
from do_comm import open_nc_valve, open_no_valve, close_nc_valve, close_no_valve, chann_disable, chann_enable, ignite
from mod_setup import do_tasks_init
import nidaqmx as ni

import threading
import random
import time
from queue import Queue, Empty
import nidaqmx
from nidaqmx.constants import AcquisitionType 
from nidaqmx.stream_readers import AnalogMultiChannelReader


sys = ni.system.System.local()   
task_list = do_tasks_init(sys)


def S1O():
    open_nc_valve(task_list[0])


def S1C():
    close_nc_valve(task_list[0])


def S2O():
    open_nc_valve(task_list[1])


def S2C():
    close_nc_valve(task_list[1])
 

def S3O():
    open_nc_valve(task_list[2])


def S3C():
    close_nc_valve(task_list[2])


def S4O():
    open_nc_valve(task_list[3])


def S4C():
    close_nc_valve(task_list[3])

   
def S5O():
    open_no_valve(task_list[4])


def S5C():
    close_no_valve(task_list[4])
   

def S6O():
    open_no_valve(task_list[5])


def S6C():
    close_no_valve(task_list[5])
   

def S7O():
    open_nc_valve(task_list[6])


def S7C():
    close_nc_valve(task_list[6])

def S8O():
    open_nc_valve(task_list[7])


def S8C():
    close_nc_valve(task_list[7])   
   
def S9O():
    chann_disable(task_list[6]) #disable he prime valve
    chann_disable(task_list[7]) #disable he fill valve
    

def S9C():
    chann_enable(task_list[6]) #enable he prime valve
    chann_enable(task_list[7]) #enable he fill valve
    
   
def S10O():
    chann_disable(task_list[8]) #disable igniter circuit

def S10C():
    chann_enable(task_list[8]) #enable igniter circuit

def S11O():
    chann_disable(task_list[2]) #disable mpva valves
    chann_disable(task_list[2]) #disable mpva valves
    chann_disable(task_list[8]) #disable igniter

def S11C():
    chann_enable(task_list[2]) #enable mpva valves
    chann_enable(task_list[2]) #enable mpva valves
    chann_enable(task_list[8]) #enable igniter

def S12O():
    open_nc_valve(task_list[3])
    time.sleep(0.25)
    open_nc_valve(task_list[2])

def S13O():
    open_no_valve(task_list[4])
    time.sleep(20)
    close_no_valve(task_list[4])

def S14O():
    close_no_valve(task_list[4])
    close_nc_valve(task_list[2])
    close_nc_valve(task_list[3])
    close_nc_valve(task_list[6])
    close_nc_valve(task_list[7])
    

tk = tk.Tk()
tk.geometry("1920x1080")
# first row
text = Label(tk, text="LRM")
text.place(x=100,y=70)
b1 = Button(tk, text="Open",width=20,height=3, command=S1O).place(x=100, y=100)
b2 = Button(tk, text="Closed",width=20,height=3,command=S1C).place(x=100, y=170)

text = Label(tk, text="HRM")
text.place(x=300,y=70)
b3 = Button(tk, text="Open",width=20,height=3, command=S2O).place(x=300, y=100)
b4 = Button(tk, text="Closed",width=20,height=3, command=S2C).place(x=300, y=170)

text = Label(tk, text="OX MPVA")
text.place(x=500,y=70)
b5 = Button(tk, text="Open",width=20,height=3, command=S3O).place(x=500, y=100)
b6 = Button(tk, text="Closed",width=20,height=3, command=S3C).place(x=500, y=170)

text = Label(tk, text="CH4 MPVA")
text.place(x=700,y=70)
b7 = Button(tk, text="Open",width=20,height=3,command=S4O).place(x=700, y=100)
b8 = Button(tk, text="Closed", width=20,height=3,command=S4C).place(x=700, y=170)

#second row
text = Label(tk, text="OB PNU")
text.place(x=100,y=250)
b10 = Button(tk, text="Open", width=20,height=3,command=S5C).place(x=100, y=280)
b9 = Button(tk, text="Closed",width=20,height=3, command=S5O).place(x=100, y=350)

text = Label(tk, text="HE VENT")
text.place(x=300,y=250)
b11 = Button(tk, text="Open",width=20,height=3, command=S6C).place(x=300, y=280)
b12 = Button(tk, text="Closed",width=20,height=3, command=S6O).place(x=300, y=350)

text = Label(tk, text="HE PRIME")
text.place(x=500,y=250)
b13 = Button(tk, text="Open",width=20,height=3, command=S7O).place(x=500, y=280)
b14 = Button(tk, text="Closed", width=20,height=3,command=S7C).place(x=500, y=350)

text = Label(tk, text="HE FILL")
text.place(x=700,y=250)
b15 = Button(tk, text="Open", width=20,height=3,command=S8O).place(x=700, y=280)
b16 = Button(tk, text="Closed", width=20,height=3,command=S8C).place(x=700, y=350)
#third row
text = Label(tk, text="PRESS SAFETY")
text.place(x=100,y=430)
b17 = Button(tk, text="On", width=20,height=3, command=S9O).place(x=100, y=460)
b18 = Button(tk, text="Off", width=20,height=3,command=S9C).place(x=100, y=530)

text = Label(tk, text="LAUNCH SAFETY")
text.place(x=300,y=430)
b19 = Button(tk, text="On",width=20,height=3, command=S10O).place(x=300, y=460)
b20 = Button(tk, text="Off",width=20,height=3,command=S10C).place(x=300, y=530)

text = Label(tk, text="IGNITER SAFETY")
text.place(x=500,y=430)
b21 = Button(tk, text="On",width=20,height=3, command=S11O).place(x=500, y=460)
b22 = Button(tk, text="Off", width=20,height=3,command=S11C).place(x=500, y=530)


b23 = Button(tk, text="Launch",width=60,height=9, bg="green", command=S12O).place(x=100, y=630)


b24 = Button(tk, text="Cycle",width=20,height=4, bg="yellow", command=S13O).place(x=700, y=460)


b24 = Button(tk, text="Abort",width=60,height=9, bg="green", command=S14O).place(x=650, y=630)
tk.mainloop()
