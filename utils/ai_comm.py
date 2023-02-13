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
		output = np.around(output, 6)
		#cont = output[4]
		#lox = output[5]

		out_psi = pressure_output = np.around(voltz_to_psi(output),6)
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
	lox_voltage = output[5]

	he_post_out_psi = (5000/8)*(he_post_out_raw-2)   #5000
	he_pre_out_psi = (7500/8)*(he_pre_out_raw-2)     #7500
	pnu_post_out_psi = (200/8)*(pnu_post_out_raw-2)  #200
	pnu_pre_out_psi = (3000/8)*(pnu_pre_out_raw-2)   #3000

	out_psi = np.vstack((he_post_out_psi, he_pre_out_psi, pnu_post_out_psi, pnu_pre_out_psi, cont_voltage, lox_voltage))
	return out_psi

def check_cont(queue, task, logger, csv_fp):
	cont = task.in_stream.open_current_loop_chans_exist()
	if cont == False:
		out = 'GOOD CONTINUITY'
	else:
		out = 'NO CONTINUITY'
	queue.put(out)
	logger.info(out)
	csv_write(out, csv_fp)


def to_csv(output, csv_file_path):
	data = output
	timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
	csv_data = [timestamp, data[0,1], data[1,1], data[2,1], data[3,1]]
	csv_write(csv_data, csv_file_path)



