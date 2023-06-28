import statistics

#fist work out mean from a set of numbers
data_set = [1, 4, 5, 7, 10, 11, 2, 8, 5]

mean = statistics.mean(data_set)
std = statistics.stdev(data_set)

print("Mean = ", mean)
print("Standard Dev = ", std)

