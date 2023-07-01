import statistics
import csv

file_path_1 = "VA.csv"

def calculate_from_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        reader.__next__() # Skip the headers in first row
        data = []
        for row in reader:
                values = float(row[0])
                data.append(values)
        
        calc_std = statistics.stdev(data)
        return calc_std

print(calculate_from_csv(file_path_1))
