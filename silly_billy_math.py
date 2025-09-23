import csv
import bisect
import math
import numpy as np
import quaternion

class Spline:
    def __init__(self, filepath):
        @staticmethod
        def csv_to_dict(filepath):
            data_dict = {}
            with open(filepath, newline='') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # skip header row
                
                for i, row in enumerate(reader):
                    # Convert each value to float
                    data_dict[i] = [float(x) for x in row]

            return data_dict
        self.dict = csv_to_dict(filepath)
        self.time_list = [row[7] for row in self.dict.values()]
        self.angle_list = [row[6] for row in self.dict.values()]

    @staticmethod
    def rows_from_dict(dict, n):
        if n < 0 or n + 1 not in dict:
            raise IndexError("Index out of range of dictionary")
        
        return [dict[n], dict[n+1]]
    
    @staticmethod
    def index_of_le(list,t):
        idt = bisect.bisect_right(list, t) - 1
        if 0 <= idt:
            return idt
        else:
            raise ValueError("Time value outside of expected range")
    
    @staticmethod
    def bezier_cubic(pos0, con0, con1, pos1, t): 
        # goes from pos0 to con0, arrives at pos1 from con1
        s = 1 - t
        return s**3 * pos0 + 3 * s**2 * t * con0 + 3 * s * t**2 * (2*pos1 - con1) + t**3 * pos1

    @staticmethod
    def bezier_cubic_derivative(pos0, con0, con1, pos1, t):
        s = 1 - t
        return 3 * s ** 2 * (con0 - pos0) + 6 * s * t * (con1 - con0) + 3 * t ** 2 * (pos1 - con1)

    def evaluate(self,t):
        #determine what segment t lies in
        section = Spline.index_of_le(self.time_list,t)

        #make a window
        array = Spline.rows_from_dict(self.dict, section)
        time0 = array[0][7]
        time1 = array[1][7]

        #normalize t between 0 and 1 on the current segment
        if time0 == time1:
            tnorm = 0
        else:
            tnorm = (t - time0) /  (time1 - time0)

        #crunch da numbers
        x = Spline.bezier_cubic(array[0][0],array[0][3],array[1][3],array[1][0],tnorm)
        y = Spline.bezier_cubic(array[0][1],array[0][4],array[1][4],array[1][1],tnorm)
        z = Spline.bezier_cubic(array[0][2],array[0][5],array[1][5],array[1][2],tnorm)

        return x,y,z
    
    def tangent_axis(self, t):
        #determine what segment t lies in
        section = Spline.index_of_le(self.time_list,t)

        #make a window
        array = Spline.rows_from_dict(self.dict, section)
        time0 = array[0][7]
        time1 = array[1][7]

        #normalize t between 0 and 1 on the current segment
        if time0 == time1:
            tnorm = 0
        else:
            tnorm = (t - time0) /  (time1 - time0)

        #crunch da numbers
        x = Spline.bezier_cubic_derivative(array[0][0],array[0][3],array[1][3],array[1][0],tnorm)
        y = Spline.bezier_cubic_derivative(array[0][1],array[0][4],array[1][4],array[1][1],tnorm)
        z = Spline.bezier_cubic_derivative(array[0][2],array[0][5],array[1][5],array[1][2],tnorm)

        return x,y,z

    def total_rotation(self,t):
        angle_list = self.angle_list
        time_list = self.time_list
        index = Spline.index_of_le(time_list,t) + 1

        if t < min(time_list) or t > max(time_list):
            raise ValueError("Time t is outside of the range of the dictionary.")
        
        if t in time_list:
            angle_list = angle_list[:index]
            time_list = [x for x in time_list if x <= t]

            return np.trapezoid(angle_list, time_list)
        
        alpha = (((angle_list[index] - angle_list[index - 1])) / (time_list[index] - time_list[index - 1])) * (t - time_list[index]) + angle_list[index]

        time_list = [x for x in time_list if x < t]
        time_list.append(t)

        angle_list = angle_list[:index]
        angle_list.append(alpha)
        
        return np.trapezoid(angle_list, time_list)
        
    def sensor_rotation(self,sensor,t): #sensor = [x,y,z]
        q0 = Quaternion.axis_angle_to_quat(self.tangent_axis(min(self.time_list)),0).normalize()
        q1 = Quaternion.axis_angle_to_quat(self.tangent_axis(t),self.total_rotation(t)).normalize()

        q = Quaternion.difference(q0,q1)

        sensor_rotated = Quaternion.rotate_vector(sensor,q)
        com = self.evaluate(t)
        x = com[0] + sensor_rotated[0]
        y = com[1] + sensor_rotated[1]
        z = com[2] + sensor_rotated[2]

        return x,y,z
        
sensor = (1,2,3)
q = np.quaternion(20,1,8,12)

print(quaternion.rotate_vectors(q,sensor))