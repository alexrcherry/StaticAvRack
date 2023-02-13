import socket
import time
import threading
import logging
from .ai_comm import ai_read
from .do_comm import open_nc_valve, open_no_valve, close_nc_valve, close_no_valve, chann_disable, chann_enable, ignite

UDP_IP = "127.0.0.1"

def cmnd_handler(run, task_list, queue_list, logger, csv_file_path ):
    UDP_PORT_RCV = 50016   #chosen port to OpenMCT (same as in telemetry server object)
    data = ''
    addr = ''
    connected = False

    # initiate socket and send first message
    sockRcv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
    try:
        sockRcv.bind((UDP_IP, UDP_PORT_RCV)) # bind the socket to the specified ip and port
        sockRcv.setblocking(0) # set the socket on unblocking, so we wont get stuck on sockRcv.recvfrom()
        connected = True # if connected go into the loop
    except:
        print('Connecting to Telemetry Server failed! Wait a couple of seconds, so the socket will close. Then restart the script.')
        sockRcv.close() # if connection fails retry

    while connected:
        try:
            data, address = sockRcv.recvfrom(1024) # buffer size is 1024 bytes
            logger.info("received message: %s" % data)
        except socket.error:
            pass
        # todo: find a better way to do this when its not 6am
        else:
            if data == ':press_safety_on':
                chann_disable(task_list[6]) #disable he prime valve
                chann_disable(task_list[7]) #disable he fill valve

            elif data == ':press_safety_off':
                chann_enable(task_list[6]) #enable he prime valve
                chann_enable(task_list[7]) #enable he fill valve

            elif data == ':igniter_safety_on':
                chann_disable(task_list[8]) #disable igniter circuit

            elif data == ':igniter_safety_off':
                chann_enable(task_list[9]) #enable igniter circuit

            elif data == ':mpv_safety_on':
                chann_disable(task_list[2]) #disable mpva valves
                chann_disable(task_list[2]) #disable mpva valves

            elif data == ':mpv_safety_off':
                chann_enable(task_list[2]) #enable mpva valves
                chann_enable(task_list[2]) #enable mpva valves

            elif data == ':launch_safety_on':
                chann_disable(task_list[2]) #disable mpva valves
                chann_disable(task_list[2]) #disable mpva valves
                chann_disable(task_list[8]) #disable igniter

            elif data == ':launch_safety_off':
                chann_enable(task_list[2]) #enable mpva valves
                chann_enable(task_list[2]) #enable mpva valves
                chann_enable(task_list[8]) #enable igniter

                #will document the rest later
            elif data == ':lrm_close':
                name = 'LRM'
                close_nc_valve(task_list[0], name, queue_list[0], csv_file_path)
            elif data == ':lrm_open':
                name = 'LRM'
                open_nc_valve(task_list[0], name, queue_list[0], csv_file_path)

            elif data == ':hrm_close':
                name = 'HRM'
                close_nc_valve(task_list[1], name, queue_list[1], csv_file_path)               
            elif data == ':hrm_open':
                name = 'HRM'
                open_nc_valve(task_list[1], name, queue_list[1], csv_file_path)

            elif data == ':mpva_ox_close':
                name = 'MPVA OX'
                close_nc_valve(task_list[2], name, queue_list[2], csv_file_path)  
            elif data == ':mpva_ox_open':
                name = 'MPVA OX'
                open_nc_valve(task_list[2], name, queue_list[2], csv_file_path)

            elif data == ':mpva_fuel_close':
                name = 'MPVA FUEL'
                close_nc_valve(task_list[3], name, queue_list[3], csv_file_path)
            elif data == ':mpva_fuel_open':
                name = 'MPVA FUEL'
                open_nc_valve(task_list[3], name, queue_list[3], csv_file_path)

            elif data == ':ob_pnu_close':
                name = 'OB PNU'
                close_no_valve(task_list[4], name, queue_list[4], csv_file_path)
            elif data == ':ob_pnu_open':
                name = 'OB PNU'
                open_no_valve(task_list[4], name, queue_list[4], csv_file_path)

            elif data == ':he_vent_close':
                name = 'HE VENT'
                close_no_valve(task_list[5], name, queue_list[5], csv_file_path)
            elif data == ':he_vent_open':
                name = 'HE VENT'
                open_no_valve(task_list[5], name, queue_list[5], csv_file_path)

            elif data == ':he_prime_close':
                name = 'HE PRIME'
                close_nc_valve(task_list[6], name, queue_list[6], csv_file_path)
            elif data == ':he_prime_open':
                name = 'HE PRIME'
                open_nc_valve(task_list[6], name, queue_list[6], csv_file_path)

            elif data == ':he_fill_close':
                name = 'HE FILL'
                close_nc_valve(task_list[7], name, queue_list[7], csv_file_path)
            elif data == ':he_fill_open':
                name = 'HE FILL'
                open_nc_valve(task_list[7], name, queue_list[7], csv_file_path)

            elif data == ':launch':
                ignite(task_list[8])
                name = 'MPVA OX'
                open_nc_valve(task_list[3], name, queue_list[3], csv_file_path)
                time.sleep(0.25) #quarter second delay that no one knows the point of
                name = 'MPVA FUEL'
                open_nc_valve(task_list[2], name, queue_list[2], csv_file_path)

            elif data == ':pressurization':
                name = 'HE PRIME'
                open_nc_valve(task_list[6], name, queue_list[6], csv_file_path)
                time.sleep(3)
                name = 'HE FILL'
                open_nc_valve(task_list[7], name, queue_list[7], csv_file_path)
                name = 'HE PRIME'
                close_nc_valve(task_list[6], name, queue_list[6], csv_file_path)
                
            elif data == ':abort':
                name = 'HE VENT'
                open_no_valve(task_list[5], name, queue_list[5], csv_file_path)
                name = 'MPVA OX'
                close_nc_valve(task_list[2], name, queue_list[2], csv_file_path)
                name = 'MPVA FUEL'
                close_nc_valve(task_list[3], name, queue_list[3], csv_file_path)
                name = 'HE FILL'
                close_nc_valve(task_list[7], name, queue_list[7], csv_file_path)
                name = 'HE PRIME'
                close_nc_valve(task_list[6], name, queue_list[6], csv_file_path)


        if not(run()): #to kill the thread
            sockRcv.close()
            print('Command Closed!')
            break


    while True:
        if not(run()): #to kill the thread
            print('Solenoid Control Closed!')
            break


def send_to_openmct(run, ai_queue, do_queue_list, cont_queue):
    UDP_PORT_SEND=50015
    MESSAGE = "23, 465, 901, 32, 7888, 2367, 1023"

    sockSend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Internet, UDP
    try:
        sockSend.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT_SEND))
    except:
        print('Initial message failed!')

    keys = [
        'pt.he_post'
        'pt.he_pre',
        'pt.pnu_post',
        'pt.pnu_pre',
        'valve.lrm', 
        'valve.hrm',
        'valve.mpva_ox',
        'valve.mpva_fuel',
        'valve.ob_pnu',
        'valve.he_vent',
        'valve.he_prime',
        'valve.he_fill', 
        'ign.continuity'] #todo: implement ignition from gse

    while True:

        timeStamp = time.time()

        pt_msg = ai_queue.get()
        lrm = do_queue_list[0].get()
        hrm = do_queue_list[1].get()
        mpva_ox = do_queue_list[2].get()
        mpva_fuel = do_queue_list[3].get()
        ob_pnu = do_queue_list[4].get()
        he_vent = do_queue_list[5].get()
        he_prime = do_queue_list[6].get()
        he_fill = do_queue_list[7].get()
        ign = cont_queue.get()
        data_pkg = [pt_msg, lrm, hrm, mpva_ox, mpva_fuel, ob_pnu, he_vent //
        he_prime, he_fill, ign]

        for k in keys:
            MESSAGE = "{},{},{}".format(k, data_pkg[k], timeStamp)
            sockSend.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT_SEND))
            print(MESSAGE)
            print('\n')

        time.sleep(0.100)

        if not(run()): #to kill the thread
            print('Socket Rx Closed!')
            break
