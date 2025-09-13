import math
import numpy as np

#hello world

class parametric_plot:    
    def position_matrix(point_1, point_2):
        matrix = np.array([point_1,point_2])
        return matrix

    def control_matrix(control_1, control_2):
        matrix = np.array([control_1,control_2])
        return matrix

    def bezier_cubic(position_matrix, control_matrix, t): 

        # goes from P0 to P1, arrives at P3 from P2
        P0 = position_matrix[0]
        P1 = control_matrix[0]
        P2 = control_matrix[1]
        P3 = position_matrix[1]

        point = (1 - t)**3 * P0 + 3 * (1-t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3

        return point

    pos_1 = (0,0)
    pos_2 = (1,1)
    control_1 = (0,1)
    control_2 = (1,0)

    test = bezier_cubic(position_matrix(pos_1, pos_2),control_matrix(control_1, control_2),1)

print(parametric_plot.test)