import nidaqmx as ni
import numpy as np
from utils import log, ai_comm, mod_setup
#from utils.ai_comm import pressure_output
from utils.mod_setup import do_tasks_init
import logging
import threading
import time
from queue import Queue
import datetime
import tkinter as tk
from tkinter import Button, Label, Canvas, Entry
import matplotlib.pyplot as plt
from matplotlib import style

from utils.do_comm import open_nc_valve, open_no_valve, close_nc_valve, close_no_valve, chann_disable, chann_enable, ignite

# init pressure, solenoid, and igniter csv files -->will log all info
timestr = time.strftime("%Y%m%d")
headers = ['timestamp', 'helium pressure[psi]', 'helium supply pressure[psi]', 'pneumatics pressure[psi]', 'pneumatics supply pressure[psi]', 'ign', 'cont']
data_csv_fp = 'logs/data_'+timestr+'.csv'
data_csv = log.init_csv_write(headers, data_csv_fp)



# initialize nidaqmx local system
sys = mod_setup.sys_init()

# create analog voltage input queue
ai_queue = Queue()
# create empty analog voltage array to be filled
ai_output = np.zeros([8, 100], dtype=np.float64)
# create empty list for valve states
valve_state = [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0]

#create lists for graphs
he = [0]*1000
he_supply = [0]*1000
pnu = [0]*1000
pnu_supply = [0]*1000
load_cell = [0]*1000

# initialize and start analog input task, for all four PT channels in pneumatics box
[ai_reader, ai_read_task] = mod_setup.ai_task_init(sys)

# create continuity reading queue
cont_queue = Queue()

# create list of valve state queues
do_queue_list = [Queue() for i in range(9)]
# initialize digital output tasks, for the 8 solenoids necessary for the LE Relaunch config
do_task_list = mod_setup.do_tasks_init(sys)

# set run mode = true
run = True

# create analog input thread
ai_thread = threading.Thread(target=ai_comm.ai_read, args=(lambda: run, ai_queue, ai_reader, ai_output, ai_read_task, data_csv_fp))
ai_thread.daemon = True
logging.info("Starting Analog Input thread")
ai_thread.start()

sys = ni.system.System.local()
task_list = do_tasks_init(sys)

import numpy as np
from matplotlib import pyplot as plt


#button functions
def S1O():
    open_nc_valve(task_list[0])
    valve_state[0] = 1


def S1C():
    close_nc_valve(task_list[0])
    valve_state[0] = 0


def S2O():
    open_nc_valve(task_list[1])
    valve_state[1] = 1


def S2C():
    close_nc_valve(task_list[1])
    valve_state[1] = 0


def S3O():
    open_nc_valve(task_list[2])
    valve_state[2] = 1


def S3C():
    close_nc_valve(task_list[2])
    valve_state[2] = 0


def S4O():
    open_nc_valve(task_list[3])
    valve_state[3] = 1


def S4C():
    close_nc_valve(task_list[3])
    valve_state[3] = 0


def S5O():
    open_no_valve(task_list[4])
    valve_state[4] = 0


def S5C():
    close_no_valve(task_list[4])
    valve_state[4] = 1


def S6O():                             #HE vent
    open_no_valve(task_list[5])
    valve_state[5] = 1


def S6C():
    close_no_valve(task_list[5])
    valve_state[5] = 0


def S7O():
    open_nc_valve(task_list[6])
    valve_state[6] = 1


def S7C():
    close_nc_valve(task_list[6])
    valve_state[6] = 0


def S8O():
    open_nc_valve(task_list[7])
    valve_state[7] = 1


def S8C():
    close_nc_valve(task_list[7])
    valve_state[7] = 0


def S9O():
    chann_disable(task_list[6])  # disable he prime valve
    chann_disable(task_list[7])  # disable he fill valve


def S9C():
    chann_enable(task_list[6])  # enable he prime valve
    chann_enable(task_list[7])  # enable he fill valve


def S10O():
    chann_disable(task_list[8])  # disable igniter circuit


def S10C():
    chann_enable(task_list[8])  # enable igniter circuit


def S11O():
    chann_disable(task_list[2])  # disable mpva valves
    chann_disable(task_list[2])  # disable mpva valves
    chann_disable(task_list[8])  # disable igniter


def S11C():
    chann_enable(task_list[2])  # enable mpva valves
    chann_enable(task_list[2])  # enable mpva valves
    chann_enable(task_list[8])  # enable igniter


def S12O():
    ignite(task_list[8])  # find out what delay should go after this
    open_nc_valve(task_list[3])
    time.sleep(0.25)
    open_nc_valve(task_list[2])

    valve_state[3] = 1
    valve_state[2] = 1


def S13O():
    def cycle():  # need to use multiprocessing library instead so that process can be killed from outside
        while True:
            dur_off = int(duration_off.get())
            dur_on = int(duration_on.get())
            open_no_valve(task_list[4])
            valve_state[4] = 1
            time.sleep(duration_on)
            close_no_valve(task_list[4])
            valve_state[4] = 0
            time.sleep(duration_off)
    # create analog input thread
    cycle_process = Process(target=cycle)
    cycle_process.daemon = True
    cycle_process.start()



def S13C():
    cycle_thread.join()




def S14O():
    open_nc_valve(task_list[0])
    open_nc_valve(task_list[1])
    close_nc_valve(task_list[2])
    close_nc_valve(task_list[3])
    open_no_valve(task_list[4])
    open_no_valve(task_list[5])
    close_nc_valve(task_list[6])
    close_nc_valve(task_list[7])
    valve_state[0] = 1
    valve_state[1] = 1
    valve_state[2] = 0
    valve_state[3] = 0
    valve_state[4] = 1
    valve_state[5] = 1
    valve_state[6] = 0
    valve_state[7] = 0


plt.ion()
plt.show()

update_rate = 10
time_list = np.arange(-len(he)/(1/(update_rate/1000)))
#print(time_list[0])
#print(time_list[-1])

def update_vals():

    #add values to the lists
    he.append(round((((sum(ai_comm.pressure_output[1])/len(ai_comm.pressure_output[1]))+ sum(he[-9:]))/10), 1))
    he_supply.append(round((((sum(ai_comm.pressure_output[3])/len(ai_comm.pressure_output[3]))+ sum(he_supply[-9:]))/10), 1))
    pnu.append(round((((sum(ai_comm.pressure_output[2])/len(ai_comm.pressure_output[2]))+ sum(pnu[-9:]))/10), 1))
    pnu_supply.append(round((((sum(ai_comm.pressure_output[0])/len(ai_comm.pressure_output[0]))+ sum(pnu_supply[-9:]))/10), 1))
    int_val = (sum(ai_comm.pressure_output[7])/len(ai_comm.pressure_output[7]))-(sum(ai_comm.pressure_output[6])/len(ai_comm.pressure_output[6]))
    int_val = int_val*83333.33333-4263.33333
    # load_cell.append((int_val + sum(load_cell[-19:]))/20)
    load_cell.append((int_val + sum(load_cell[-19:]))/20)
    #remove first value from list if list is at length
    if (len(he) > 1000):
        he.pop(0)
        he_supply.pop(0)
        pnu.pop(0)
        pnu_supply.pop(0)
        load_cell.pop(0)
    #
    val0 = 'HE: ' + str(he[-1]) + 'psi'
    val1 = 'HE Supply: ' + str(he_supply[-1]) + 'psi'
    val2 = 'Pneumatics: ' + str(pnu[-1]) + 'psi'
    val3 = 'Pneumatics Supply: ' + str(pnu_supply[-1]) + 'psi'
    val4 = round(sum(ai_comm.pressure_output[4])/len(ai_comm.pressure_output[4]), 1)
    val5 = round(sum(ai_comm.pressure_output[5])/len(ai_comm.pressure_output[5]), 1)
    load_cell_1 = 'sig+:' + str(round(sum(ai_comm.pressure_output[6])/len(ai_comm.pressure_output[6]), 6))
    load_cell_2 = 'sig-:' + str(round(sum(ai_comm.pressure_output[7])/len(ai_comm.pressure_output[7]), 6))


    if val4 > 3:
        val4 = 'Ematch: No Continuity:' + str(val4)
    else:
        val4 = 'Ematch: Continuity:' + str(val4)

    if val5 > 3:
        val5 = 'Breakwire: No Continuity:' + str(val5)
    else:
        val5 = 'Breakwire: Continuity:' + str(val5)

    plt.clf()
    # plt.plot(range(len(he)), he, label = 'He')
    # plt.plot(range(len(he_supply)), he_supply, label = 'He Supply')
    # plt.plot(range(len(pnu)), pnu, label = 'Pneumatics')
    # plt.plot(range(len(pnu_supply)), pnu_supply, label = 'Pneumatics Supply')
    plt.plot(range(len(load_cell)), load_cell, label = 'Load Cell')
    plt.xlabel("Time (Sec)")
    plt.ylabel("Pressure (Psi)")
    plt.title("Ground Systems Pressure")
    plt.legend()
    plt.draw()

   

    #plt.pause(0.001)


    time_val = datetime.datetime.now().strftime("Time: %H:%M:%S")
    label0.config(text=val0)
    label1.config(text=val1)
    label2.config(text=val2)
    label3.config(text=val3)
    label4.config(text=val4)

    label5.config(text=val5)
    label6.config(text=load_cell_1)
    label7.config(text=load_cell_2)

    time_lab.config(text=time_val)

    if valve_state[0] == 1:
        myCanvas.itemconfig(ind_0, fill = 'green')
    else:
        myCanvas.itemconfig(ind_0, fill = 'red')

    if valve_state[1] == 1:
        myCanvas.itemconfig(ind_1, fill = 'green')
    else:
        myCanvas.itemconfig(ind_1, fill = 'red')

    if valve_state[2] == 1:
        myCanvas.itemconfig(ind_2, fill = 'green')
    else:
        myCanvas.itemconfig(ind_2, fill = 'red')

    if valve_state[3] == 1:
        myCanvas.itemconfig(ind_3, fill = 'green')
    else:
        myCanvas.itemconfig(ind_3, fill = 'red')

    if valve_state[4] == 0:
        myCanvas.itemconfig(ind_4, fill = 'green')
    else:
        myCanvas.itemconfig(ind_4, fill = 'red')

    if valve_state[5] == 1:
        myCanvas.itemconfig(ind_5, fill = 'green')
    else:
        myCanvas.itemconfig(ind_5, fill = 'red')

    if valve_state[6] == 1:
        myCanvas.itemconfig(ind_6, fill = 'green')
    else:
        myCanvas.itemconfig(ind_6, fill = 'red')

    if valve_state[7] == 1:
        myCanvas.itemconfig(ind_7, fill = 'green')
    else:
        myCanvas.itemconfig(ind_7, fill = 'red')

    tk.after(update_rate, update_vals)


tk = tk.Tk()
S6O()
tk.geometry("1920x1080")
tk.title('Control Panel')


myCanvas = Canvas(tk, height = 600, width = 1000)
myCanvas.place(x=0,y=0)
def create_circle(x,y,r,canvas, **kwargs):
	return canvas.create_oval(x-r,y-r,x+r, y+r, **kwargs)
#indicators
ind_0 = create_circle(95, 78, 4, myCanvas, fill= 'blue')
ind_1 = create_circle(295, 78, 4, myCanvas, fill= 'blue')
ind_2 = create_circle(495, 78, 4, myCanvas, fill= 'blue')
ind_3 = create_circle(695, 78, 4, myCanvas, fill = 'blue')
ind_4 = create_circle(95, 258, 4, myCanvas, fill = 'blue')
ind_5 = create_circle(295, 258, 4, myCanvas, fill = 'blue')
ind_6 = create_circle(495, 258, 4, myCanvas, fill = 'blue')
ind_7 = create_circle(695, 258, 4, myCanvas, fill = 'blue')
#text for pres data
time_lab = Label(tk)
time_lab.place(x=10,y=10)

label0 = Label(tk)
label0.place(x=1000,y=70)

label1 = Label(tk)
label1.place(x=1200,y=70)

label2 = Label(tk)
label2.place(x=1400,y=70)

label3 = Label(tk)
label3.place(x=1600,y=70)

label4 = Label(tk)
label4.place(x=1000,y=140)

label5 = Label(tk)
label5.place(x=1200,y=140)

label6 = Label(tk)
label6.place(x=1400,y=140)

label7 = Label(tk)
label7.place(x=1600,y=140)

update_vals()




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
text = Label(tk, text="Onboard Vents")
text.place(x=100,y=250)
b10 = Button(tk, text="Open", width=20,height=3,command=S5O).place(x=100, y=280)
b9 = Button(tk, text="Closed",width=20,height=3, command=S5C).place(x=100, y=350)

text = Label(tk, text="HE VENT")
text.place(x=300,y=250)
b11 = Button(tk, text="Open",width=20,height=3, command=S6O).place(x=300, y=280)
b12 = Button(tk, text="Closed",width=20,height=3, command=S6C).place(x=300, y=350)

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


b23 = Button(tk, text="Launch", font='Helvetica 18 bold',width=60,height=9, bg="green", command=S12O).place(x=100, y=630)


b24 = Button(tk, text="Vent Cycle On", width=20, height=3, bg="yellow", command=S13O).place(x=700, y=460)
b25 = Button(tk, text="Vent Cycle Off", width=20, height=3, bg="yellow", command=S13C).place(x=700, y=530)
duration_label1 = Label(tk, text='Duration On (S):').place(x=900, y=460)
duration_label2 = Label(tk, text='Duration Off (S):').place(x=900, y=530)
duration_on = Entry(tk).place(x=1000, y=460)
duration_off = Entry(tk).place(x=1000, y=530)


b26 = Button(tk, text="Abort", font='Helvetica 18 bold', width=60, height=9, bg="red", command=S14O).place(x=850, y=630)
tk.mainloop()
