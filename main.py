import statistics
import csv
import os

file_path_1 = "VA.csv"
file_path_2 = "MX.csv"

#error handling
def does_file_exist(file_path):
    if os.path.exists(file_path):
        return True
    else:
        raise Exception(f"{file_path} does not exist")


def calculate_from_csv(file_path):
    with open(file_path, 'r') as f: #'r' to read content of csv
        reader = csv.reader(f)
        reader.__next__() # Skip the headers in first row
        data = []
        for row in reader:
                values = float(row[0])
                data.append(values)
        
        calc_std = statistics.stdev(data)
        return calc_std


try: 
    print(calculate_from_csv(file_path_1))
    print(calculate_from_csv(file_path_2))
except Exception as error:
     print(str(error))

