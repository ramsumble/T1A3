import statistics
import csv
import os

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
        # reader.__next__() 
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
        return calc_std

output_value = calculate_from_csv(file_path_1)

#create the csv is none exists, append the calc value to new csv
def output_csv(file_path):
    with open("output.csv", "a") as file: # "a" to append
        file.write(f"\n{output_value}")#write() can only write strings - not sure if there is a better way
    return file_path


try: 
    output_csv(output_file)
    print(calculate_from_csv(file_path_1))
    print(calculate_from_csv(file_path_2))

except Exception as error:
     print(error)



# TODO
# add calc for mean
# calc second csv 
# add date/time 