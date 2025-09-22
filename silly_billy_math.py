import csv
import bisect
import math

class Quaternion:
    def __init__(self,x,y,z,w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def output_as_list(self):
        return [self.x, self.y, self.z, self.w]
    
    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)
    
    def normalize(self):
        m = self.magnitude()
        if m == 0:
            return Quaternion(0,0,0,0)
        return Quaternion(self.x / m, self.y / m, self.z / m, self.w / m)
    
    @staticmethod
    def identity():
        return Quaternion(0,0,0,1)
    
    def scale(self, s: float):
        return Quaternion(self.x * s, self.y * s, self.z * s, self.w * s)
    
    @classmethod
    def mult(cls, a, b):
        if not isinstance(a, cls) or not isinstance(b, cls):
            raise TypeError("Both inputs must be instances of the Quaternion class.")
        return Quaternion(a.w * b.x + a.x * b.w + a.y * b.z - a.z * b.y, a.w * b.y - a.x * b.z + a.y * b.w + a.z * b.x, a.w*b.z + a.x*b.y - a.y*b.x + a.z*b.w, a.w*b.w - a.x*b.x - a.y*b.y - a.z*b.z)
    
    @staticmethod
    def axis_angle_to_quat(axis, angle): #axis = [x,y,z]
        s = math.sin(angle / 2)
        return Quaternion(axis[0] * s, axis[1] * s, axis[2] * s, math.cos(angle / 2))
    
    def conjugate(self):
        return Quaternion(-self.x,-self.y,-self.z,self.w)
    
    @classmethod
    def rotate_vector(cls, v, q): #v = [x,y,z]
        if not isinstance(q, cls):
            raise TypeError("q must be an instance of the Quaternion class.")
        v = Quaternion(v[0],v[1],v[2],0)
        v = Quaternion.mult(Quaternion.mult(q,v), q.conjugate())
        return [v.x, v.y, v.z]

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
        point = (1 - t)**3 * pos0 + 3 * (1-t)**2 * t * con0 + 3 * (1 - t) * t**2 * (2*pos1 - con1) + t**3 * pos1

        return point

    def bezier_spline(self,t):
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
        x = Spline.bezier_cubic(array[0][0],array[0][3],array[1][0],array[1][3],tnorm)
        y = Spline.bezier_cubic(array[0][1],array[0][4],array[1][1],array[1][4],tnorm)
        z = Spline.bezier_cubic(array[0][2],array[0][5],array[1][2],array[1][5],tnorm)

        return x,y,z
        
