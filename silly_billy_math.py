import csv
import bisect
import numpy as np
import math

class Quaternion:
    def __init__(self,x,y,z,w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def output_as_list(self):
        quat = [self.x, self.y, self.z, self.w]
        return quat
    
    def magnitude(self):
        m = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)
        return m
    
    def normalize(self):
        m = self.magnitude()
        if m == 0:
            quat = Quaternion(0,0,0,0)
            return quat
        quat = Quaternion(self.x / m, self.y / m, self.z / m, self.w / m)
        return quat
    
    @staticmethod
    def identity():
        quat = Quaternion(0,0,0,1)
        return quat
    
    def scale(self, s: float):
        quat = Quaternion(self.x * s, self.y * s, self.z * s, self.w * s)
        return quat
    
    @classmethod
    def mult(cls, a, b):
        if not isinstance(a, cls) or not isinstance(b, cls):
            raise TypeError("Both inputs must be instances of the Quaternion class.")
        quat = Quaternion(a.w*b.x + a.x*b.w + a.y*b.z - a.z*b.y,
                        a.w*b.y - a.x*b.z + a.y*b.w + a.z*b.x,
                        a.w*b.z + a.x*b.y - a.y*b.x + a.z*b.w,
                        a.w*b.w - a.x*b.x - a.y*b.y - a.z*b.z)
        return quat
    
    @staticmethod
    def axis_angle_to_quat(axis, angle): #axis = [x,y,z]
        s = math.sin(angle / 2)
        quat = Quaternion(axis[0] * s, axis[1] * s, axis[2] * s, math.cos(angle / 2))
        return quat
    
    def conjugate(self):
        quat = Quaternion(-self.x,-self.y,-self.z,self.w)
        return quat
    
    @classmethod
    def rotate_vector(cls, v, q): #v = [x,y,z]
        if not isinstance(q, cls):
            raise TypeError("q must be an instance of the Quaternion class.")
        v = Quaternion(v[0],v[1],v[2],0)
        v = Quaternion.mult(Quaternion.mult(q,v), q.conjugate())
        vec = [v.x, v.y, v.z]
        return vec
    
    def inverse(self):
        m = self.magnitude()
        if m == 0:
            return Quaternion(0,0,0,0)
        m *= m
        quat = Quaternion(-self.x / m, -self.y / m, -self.z / m, self.w / m)
        return quat
    
    @classmethod
    def difference(cls, a, b):
        if not isinstance(a, cls) or not isinstance(b, cls):
            raise TypeError("Both inputs must be instances of the Quaternion class.")
        quat = Quaternion.mult(a.inverse(), b)
        return quat

class Spline:
    def __init__(self, filepath):
        @staticmethod
        def csv_to_dict(filepath):
            data_dict = {}
            try:
                with open(filepath, newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    headers = next(reader)  # skip header row
                    
                    for i, row in enumerate(reader):
                        # Convert each value to float
                        data_dict[i] = [float(x) for x in row]

                return data_dict
            except:
                raise TypeError('Inputted file must be a csv')
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
        path = s**3 * pos0 + 3 * s**2 * t * con0 + 3 * s * t**2 * (2*pos1 - con1) + t**3 * pos1
        return path

    @staticmethod
    def bezier_cubic_derivative(pos0, con0, con1, pos1, t): #P0,P1,P2,P3
        path = -3 * (1 - t)**2 * pos0 + 3 * (1 - 4*t + 3*t**2)*con0 + 3 * (2 * t - 3 * t**2) * (2 * pos1 - con1) + 3*t**2 * pos1
        return path

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

        #normalize output
        m = np.sqrt(x*x + y*y + z*z)

        axis = x/m, y/m, z/m

        return axis

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
        
        rotation = np.trapezoid(angle_list, time_list)

        return rotation
        
    def sensor(self,sensor,t):
        axis0 = self.tangent_axis(min(self.time_list))
        axis1 = self.tangent_axis(t)
        cross = np.cross(axis0,axis1)

        q0 = Quaternion(cross[0],cross[1],cross[2], 1 + np.dot(axis0,axis1)).normalize()
        q1 = Quaternion.axis_angle_to_quat(self.tangent_axis(t),self.total_rotation(t))
        w = Quaternion.mult(q1,q0)

        rotated_sensor = Quaternion.rotate_vector(sensor,w)
        translation = self.evaluate(t)
        x = rotated_sensor[0] + translation[0]
        y = rotated_sensor[1] + translation[1]
        z = rotated_sensor[2] + translation[2]

        return x,y,z
