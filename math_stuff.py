import math
import numpy as np

class math_functions:
    def __init__(self):
        #initialize

    def bezier_cubic(P0, P1, P2, P3, t): # goes from P0 to P1, arrives at P3 from P2
        point = (1 - t)**3 * P0 + 3 * (1-t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3

        return point
