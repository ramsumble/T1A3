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
            groups["10"].append(number)
        elif number < 10:
            numbers_under_10[number] += 1

    group_counts = {}
    for group, numbers in groups.items():
        count = len(numbers)
        group_counts[group] = count

    group_counts.update(numbers_under_10)

    return group_counts

data = read_csv(file_path_1, delimiter=",")
result = group_up_numbers(data)

# grab the key values from dict for plotting
labels = list(result.keys())
counts = list(result.values())

labels = [str(label) for label in labels] # Convert labels to strings for the bar graph

def plot_data(file):
    plt.bar(labels, counts)
    plt.xlabel('Triggers')
    plt.ylabel('Count')
    plt.title('Number of triggers')
    plt.show()


try: 
    output_csv(output_file)
    print("VA score = ",calculate_from_csv(file_path_1))
    print("MX score = ",calculate_from_csv(file_path_2))
    plot_data(file_path_1)

except Exception as error:
     print(error)


# TODO
# combine both dicts so they can be displayed a single bar graph 
# BONUS
# add a way to mass calculate multiple csv's of the same dataset
# print the top outliers - need to workout is there is math behind calculating an outlier
