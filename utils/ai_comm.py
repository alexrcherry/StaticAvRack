from contextlib import contextmanager
import numpy as np
import nidaqmx as ni
import queue
from .log import csv_write
from datetime import datetime

# for analog input thread
def ai_read(run, queue, reader, output, task, csv_file_path):
	global pressure_output
	#global cont
	while True:
		reader.read_many_sample(output, number_of_samples_per_channel=100)
		
		#cont = output[4]
		#lox = output[5]

		out_psi = pressure_output = voltz_to_psi(output)
		queue.put((out_psi))
		to_csv(out_psi, csv_file_path)
		# check_cont(queue_cont, task, logger_cont, csv_file_path_cont)

		if not (run()):  # to kill the thread
			print('AI input thread closed!')
			break


def voltz_to_psi(output):

	#split up analog voltage output data for each pressure transducer, based on hardware setup
	he_post_out_raw = output[0]	  # ai0: helium pressure, 0-5000psi
	he_pre_out_raw = output[1] 	  # ai1: helium supply pressure, 0-7500psi
	pnu_post_out_raw = output[2]  # ai2: pneumatics pressure, 0-200psi
	pnu_pre_out_raw = output[3]	  # ai3: pneumatics supply pressure, 0-3000psi
	cont_voltage = output[4]
	breakwire = output[5]
	load_cell_0 = output[6]
	load_cell_1 = output[7]

	he_post_out_psi = 1840.1*(he_post_out_raw)-3920.2   #5000
	he_pre_out_psi = 2240.7*(he_pre_out_raw)-4461.8     #7500
	pnu_post_out_psi = (200/8)*(pnu_post_out_raw-2)  #200
	pnu_pre_out_psi = 375*(pnu_pre_out_raw)-750   #3000

	out_psi = np.vstack((he_post_out_psi, he_pre_out_psi, pnu_post_out_psi, pnu_pre_out_psi, cont_voltage, breakwire, load_cell_0, load_cell_1))
	return out_psi


def to_csv(output, csv_file_path):
	data = output
	timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	csv_data = [timestamp, data[0,1], data[1,1], data[2,1], data[3,1]]
	csv_write(csv_data, csv_file_path)



