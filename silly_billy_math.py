import csv
import bisect

#make a dictionary from the csv (this method i found online doesnt use pandas, but it works so im not gonna mess with it)
def csv_to_dict(filename):
    data_dict = {}
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # skip header row
        
        for i, row in enumerate(reader):
            # Convert each value to float
            data_dict[i] = [float(x) for x in row]
    
    return data_dict

#extract the n and n+1 rows from the dict
def get_rows_from_dict(data_dict, n):
    if n < 0 or n+1 not in data_dict:
        raise IndexError("Index out of range for selecting rows.")
    
    return [data_dict[n], data_dict[n+1]]

#helper function
def index_of_le(list,t):
    idt = bisect.bisect_right(list, t) - 1
    if 0 <= idt:
        return idt
    else:
        raise ValueError("Time value outside of expected range")

#cubic bezier curve eq
def bezier_cubic(pos0, con0, con1, pos1, t): 
    # goes from pos0 to con0, arrives at pos1 from con1
    point = (1 - t)**3 * pos0 + 3 * (1-t)**2 * t * con0 + 3 * (1 - t) * t**2 * (2*pos1 - con1) + t**3 * pos1

    return point

#patch those bitches together
def bezier_spline(t):
    #determine what section t lies in
    time_list = [row[7] for row in point_dict.values()]
    section = index_of_le(time_list,t)
    
    array = get_rows_from_dict(point_dict,section)
    time0 = array[0][7]
    time1 = array[1][7]
    #normalize t between 0,1 for current segment
    if time0 == time1:
        tnorm = 0
    else:
        tnorm = (t - time0) /  (time1 - time0)

    if time0 <= t <= time1:
        x = bezier_cubic(array[0][0],array[0][3],array[1][0],array[1][3],tnorm)
        y = bezier_cubic(array[0][1],array[0][4],array[1][1],array[1][4],tnorm)
        z = bezier_cubic(array[0][2],array[0][5],array[1][2],array[1][5],tnorm)

    return x,y,z

#############################
#this section should be the main loop?
#the dictionary needs to be established outside the function 
#which i think is something doable inside a class
file_path = "sample.csv"
point_dict = csv_to_dict(file_path)

#the argument for bezier_spline can range from the lowest to largest value in the time column
#print(bezier_spline(2.9))

