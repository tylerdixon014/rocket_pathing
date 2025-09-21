import math
import numpy as np
import csv

file_path = "sample.csv"

def csv_to_dict(filename):
    """
    Reads a CSV file into a dictionary.
    Keys = row index (0-based), Values = list of floats for that row.
    
    Parameters:
        filename (str): Path to the CSV file.
    
    Returns:
        dict: Dictionary of rows with index as key.
    """
    data_dict = {}
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # skip header row
        
        for i, row in enumerate(reader):
            # Convert each value to float
            data_dict[i] = [float(x) for x in row]
    
    return data_dict

def get_rows_from_dict(data_dict, n):
    """
    Returns rows n and n+1 from a dictionary created by csv_to_dict.
    
    Parameters:
        data_dict (dict): Dictionary of rows from csv_to_dict.
        n (int): Row index (0-based).
    
    Returns:
        list: List containing rows n and n+1 as lists of floats.
    """
    if n < 0 or n+1 not in data_dict:
        raise IndexError("Index out of range for selecting rows.")
    
    return [data_dict[n], data_dict[n+1]]

def bezier_cubic(pos0, con0, con1, pos1, t): # goes from pos0 to con0, arrives at pos1 from con1
    point = (1 - t)**3 * pos0 + 3 * (1-t)**2 * t * con0 + 3 * (1 - t) * t**2 * con1 + t**3 * pos1

    return point

def bezier_spline(filename, t):
    point_dict = csv_to_dict(filename)
    i = 0
    while i <= len(point_dict) - 2:
        array = get_rows_from_dict(point_dict,i)
        x = bezier_cubic(array[0][0],array[0][3],array[1][0],array[1][3],t)
        y = bezier_cubic(array[0][1],array[0][4],array[1][1],array[1][4],t)
        z = bezier_cubic(array[0][2],array[0][5],array[1][2],array[1][5],t)

        print(x,y,z)

        i += 1

bezier_spline(file_path,0)