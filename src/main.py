import statistics
import csv
import os
# import matplotlib # used for venv to save graphs
# matplotlib.use('Agg') # used for venv to save graphs
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import seaborn as sns
import datetime
from collections import Counter
import cowsay


file_path_1 = "./input/VA.csv"
file_path_2 = "./input/MX.csv"
output_file = "output.csv"


#error handling for missing files
def does_file_exist(file_path):
    if os.path.exists(file_path):
        return True
    else:
        raise Exception(f"{file_path} does not exist")


def calculate_from_csv(file_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    relative_file_path = os.path.join(current_dir, file_path)
    
    with open(relative_file_path, "r") as f: #"r" to read content of csv
        reader = csv.reader(f)
        next(reader) # Skip the headers in first row
        data = []
        for row in reader:
                values = row[2]
                if values != "null": 
                    try:
                        values = float(values)
                        data.append(values)
                    except ValueError: #error handling for non numberic values
                        print(f"There is a value in {file_path} that is not vaild, value ignored")
        
        calc_std = statistics.stdev(data) #thank you statistics for making this easy
        calc_mean = statistics.mean(data)
        return calc_std, calc_mean


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
            groups["10+"].append(number)
        elif number < 10: # this will append as an int!
            numbers_under_10[number] += 1

    group_counts = {}
    for group, numbers in groups.items():
        count = len(numbers)
        group_counts[group] = count

    group_counts.update(numbers_under_10)

    return group_counts


def combine_data_into_dict(va_dict, mx_dict):
    #had to correct dict as the for loop in group_up_numbers will create the Keys as integers
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
        combined_dict[k][0] = v # add to the first key index

    for k, v in mx_dict.items():
        combined_dict[k][1] = v # add to the second key index

    return combined_dict

# graphs information was all sourced from https://python-graph-gallery.com/

# https://python-graph-gallery.com/grouped-barplot/ 
def create_bar_graph(combined_dict):
    #styling with Seaborn
    colors = ["#69b3a2", "#4374B3"]
    sns.set_palette(sns.color_palette(colors))
    sns.set(style="darkgrid")

    
    labels = combined_dict.keys()
    values_va = [item[0] for item in combined_dict.values()]
    values_mx = [item[1] for item in combined_dict.values()]
   
    x = np.arange(len(labels))
    width = 0.4 # width of bars 

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, values_va, width, label='VA Data')
    rects2 = ax.bar(x + width/2, values_mx, width, label='MX Data')

    ax.set_xlabel('Triggers')
    ax.set_ylabel('Count')
    ax.set_title('VA vs MX')
    ax.set_xticks(x) # used together for labelling the x axis
    ax.set_xticklabels(labels) # used together for labelling the x axis
    ax.legend()
    
    plt.savefig('Bar.png') 
    plt.show() # not compatible with the venv

# https://python-graph-gallery.com/line-chart/
def create_line_graph(combined_dict):
    #styling with Seaborn
    colors = ["#69b3a2", "#4374B3"]
    sns.set_palette(sns.color_palette(colors))
    sns.set(style="darkgrid")

    labels = combined_dict.keys()
    values_va = [item[0] for item in combined_dict.values()]
    values_mx = [item[1] for item in combined_dict.values()]
    
    x = np.arange(len(labels))

    fig, ax = plt.subplots()
    ax.plot(values_va, label='VA Data')
    ax.plot(values_mx, label='MX Data')

    ax.set_xlabel('Triggers')
    ax.set_ylabel('Count')
    ax.set_title('VA vs MX')
    ax.set_xticks(x) # used together for labelling the x axis
    ax.set_xticklabels(labels) # used together for labelling the x axis
    ax.legend()

    plt.savefig('Line.png')  
    plt.show() # not compatible with the venv

# # https://python-graph-gallery.com/boxplot/
# box plot doesnt seem feasible with current datasets 
# def create_box_plot(combined_dict):
#     sns.set(style="darkgrid")

#     # data_va = [item[0] for item in combined_dict.values()]
#     # data_mx = [item[1] for item in combined_dict.values()]

#     data = [va_data, mx_data]
#     labels = ['VA Data', 'MX Data']

#     sns.boxplot(data=data) # crazy easy with seaborn!
#     plt.xlabel('Triggers')
#     plt.ylabel('Count')
#     plt.title('VA vs MX')

#     plt.show()    

try:
    user_input = input(cowsay.cow(("\n Which graph would you like to display? \n For the Line graph: Line \n For the Bar graph: Bar\n"))) # need to fix user_input on interupt
    user_input2 = input(cowsay.cow(("\n Would you like to see the score in the output? \nYes/No "))) # need to fix user_input on interupt
    output = cowsay.cow(f"you have selected: \n{user_input} \n{user_input2}")
except KeyboardInterrupt:
    print("\nKeyboardIntterupt!")
    print(cowsay.cow("Goodbye!"))

# store the output of calculate_from_csv into variables
output_value_VA = str(calculate_from_csv(file_path_1))
output_value_MX = str(calculate_from_csv(file_path_2))

# remove perenthesis from output which will be appended to output.csv
VA_value = output_value_VA.replace('(','').replace(')','')
MX_value = output_value_MX.replace('(','').replace(')','')

# get only the relevant data from csv's
va_data = read_csv(file_path_1, ",")
mx_data = read_csv(file_path_2, ",")

# group data into dictionaries
group_va = group_up_numbers(va_data)
group_mx = group_up_numbers(mx_data)

# combine the dictionaries into a single dict for graphs 
combined_dict = combine_data_into_dict(group_va, group_mx)
    

try:
    output_csv(output_file)
    # create_box_plot(va_data) # we dont want to measure the consolidated data with the box plot
    if user_input == "Line":
        create_line_graph(combined_dict)
    elif user_input == "Bar":
        create_bar_graph(combined_dict)
    else:
        raise ValueError("Invalid input, please enter either Line or Bar")  
    if user_input2 == "Yes":
        print("VA score = ",calculate_from_csv(file_path_1))
        print("MX score = ",calculate_from_csv(file_path_2))
    elif user_input2 == "No":
        print(cowsay.cow("Goodbye!"))
    else:
        raise ValueError("Please enter either Yes or No")
except ValueError as v_Error:
    print(v_Error)
except Exception as e_error:
    print(e_error)


# TODO
# check to see if error handling can be improved
# maybe implement --help features
