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

q = Quaternion.identity()
v = [20,30,1]
w = Quaternion.rotate_vector(v,q)
print(w)
