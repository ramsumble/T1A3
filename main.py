import statistics
import csv
import os
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import seaborn as sns
import datetime

file_path_1 = "VA.csv"
file_path_2 = "MX.csv"
output_file = "output.csv"

#error handling for missing files
def does_file_exist(file_path):
    if os.path.exists(file_path):
        return True
    else:
        raise Exception(f"{file_path} does not exist")


def calculate_from_csv(file_path):
    with open(file_path, "r") as f: #"r" to read content of csv
        reader = csv.reader(f)
        next(reader) # Skip the headers in first row
        data = []
        for row in reader:
                values = row[2]
                if values != "null":
                    try:
                        values = float(values)
                        data.append(values)
                    except ValueError:
                        pass
        
        calc_std = statistics.stdev(data)
        calc_mean = statistics.mean(data)
        return calc_std, calc_mean

output_value_VA = calculate_from_csv(file_path_1)
output_value_MX = calculate_from_csv(file_path_2)

#create the csv is none exists, append the calc value to new csv
def output_csv(file_path):
    with open("output.csv", "a") as file: # "a" to append
        headerlist = ["Date","VA Std", "VA Mean", "MX Std", "MX Mean"]
        file_is_empty = os.stat(file_path).st_size == 0 #determine if file is empty, only used for the header
        date = datetime.date.today()
        if file_is_empty:
            dw = csv.DictWriter(file, delimiter=",", fieldnames=headerlist)
            dw.writeheader()
        file.write(f"{date},{output_value_VA},{output_value_MX}\n")#write() can only write strings - not sure if there is a better way
    return file_path


def read_csv(file, delimiter):
    list_third_column = []
    with open(file, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        data = list(reader)
        for item in reversed(data): #some reason need to reverse data to display properly 
            if item[2] != "null": #ignore null values 
                list_third_column.append(item[2])
    return list_third_column


def plot_data(file):
    sns.set_theme() # added a theme so the graph is a little easier to digest 
    data = read_csv(file, ",")
    plt.plot(data)
    plt.show()

try: 
    output_csv(output_file)
    print("VA score = ",calculate_from_csv(file_path_1))
    print("MX score = ",calculate_from_csv(file_path_2))
    # plot_data(file_path_1)

except Exception as error:
     print(error)


# TODO
# add date/time 
# correct the output, be in seperate cells 
# add help function if applicable
# BONUS
# add a way to mass calculate multiple csv's of the same dataset
# print the top outliers - need to workout is there is math behind calculating an outlier
