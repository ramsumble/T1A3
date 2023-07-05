import statistics
import csv
import os
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import seaborn as sns
import datetime
from collections import Counter


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
        
        calc_std = statistics.stdev(data) #thank you statistics for making this easy
        calc_mean = statistics.mean(data)
        return calc_std, calc_mean

output_value_VA = str(calculate_from_csv(file_path_1))
output_value_MX = str(calculate_from_csv(file_path_2))

#remove perenthesis from output
VA_value = output_value_VA.replace('(','').replace(')','')
MX_value = output_value_MX.replace('(','').replace(')','')

#create the csv if none exists, append the calc value to new csv
def output_csv(file_path):
    with open("output.csv", "a") as file: # "a" to append
        headerlist = ["Date","VA Std", "VA Mean", "MX Std", "MX Mean"]
        file_is_empty = os.stat(file_path).st_size == 0 #determine if file is empty, only used for the header
        date = datetime.date.today()
        if file_is_empty:
            dw = csv.DictWriter(file, delimiter=",", fieldnames=headerlist)
            dw.writeheader()
        file.write(f"{date},{VA_value},{MX_value}\n")#write() can only write strings - not sure if there is a better way
    return file_path

def read_csv(file, delimiter):
    list_third_column = []
    with open(file, newline='') as f:
        reader = csv.reader(f)
        next(reader) # skip header
        data = list(reader)
        for item in data: 
            if item[2] != "null": #ignore null values 
                list_third_column.append(int(item[2])) 
    return list_third_column

va_data = read_csv(file_path_1, ",")
mx_data = read_csv(file_path_2, ",")

def group_up_numbers(data):
    numbers_under_10 = Counter()
    for number in data:
        if number < 10:
            numbers_under_10[number] += 1

    groups = {
        "200+": [],
        "100+": [],
        "50+": [],
        "20+": [],
        "10+": [],    
    }
    for number in data:
        if number > 200:
            groups["200+"].append(number)
        elif number >= 100:
            groups["100+"].append(number)
        elif number >= 50:
            groups["50+"].append(number)
        elif number >= 20:
            groups["20+"].append(number)
        elif number >= 10:
            groups["10+"].append(number)
        elif number < 10:
            numbers_under_10[number] += 1

    group_counts = {}
    for group, numbers in groups.items():
        count = len(numbers)
        group_counts[group] = count

    group_counts.update(numbers_under_10)

    return group_counts

group_va = group_up_numbers(va_data)
group_mx = group_up_numbers(mx_data)

def combine_data_into_dict(va_dict, mx_dict):
    combined_dict = {
        "200+": [0, 0],
        "100+": [0, 0],
        "50+": [0, 0],
        "20+": [0, 0],
        "10+": [0, 0],
        9: [0, 0],
        8: [0, 0],
        7: [0, 0],
        6: [0, 0],
        5: [0, 0],
        4: [0, 0],
        3: [0, 0],
        2: [0, 0],
        1: [0, 0],
        0: [0, 0]
    }

    for k, v in va_dict.items():
        combined_dict[k][0] = v

    for k, v in mx_dict.items():
        combined_dict[k][1] = v

    return combined_dict


def create_bar_graph(combined_dict):
    labels = combined_dict.keys()
    values_va = [item[0] for item in combined_dict.values()]
    values_mx = [item[1] for item in combined_dict.values()]
   
    x = np.arange(len(labels))
    width = 0.4

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, values_va, width, label='VA Data')
    rects2 = ax.bar(x + width/2, values_mx, width, label='MX Data')

    ax.set_xlabel('Categories')
    ax.set_ylabel('Counts')
    ax.set_title('Combined Data')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.show()

combined_dict = combine_data_into_dict(group_va, group_mx)


try: 
    output_csv(output_file)
    print("VA score = ",calculate_from_csv(file_path_1))
    print("MX score = ",calculate_from_csv(file_path_2))
    create_bar_graph(combined_dict)

except Exception as error:
     print(error)


# TODO
# create line graph with combined data
