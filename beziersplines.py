import csv
import bisect

file = "sample.csv"

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
        
spline = Spline(file)
print(spline.bezier_spline(9))