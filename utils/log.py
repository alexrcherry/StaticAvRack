import logging
import csv

def init_csv_write(csv_headers, csv_file_path):
    with open(csv_file_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)

def csv_write(csv_data, csv_file_path):
    with open(csv_file_path, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(csv_data)


