import csv
import bisect
from dataclasses import dataclass

@dataclass
class Knot:
    x: float
    y: float
    z: float
    cx: float   # control point leaving this knot
    cy: float
    cz: float
    t: float    # time

class BezierSpline:
    def __init__(self, csv_path: str):
        self.knots = self._load_csv(csv_path)
        if len(self.knots) < 2:
            raise ValueError("Need at least two rows (knots) to form a segment.")
        self.times = [k.t for k in self.knots]
        if self.times != sorted(self.times):
            raise ValueError("Time column (7th) must be nondecreasing.")

    @staticmethod
    def _load_csv(filename: str):
        rows = []
        with open(filename, newline='') as f:
            r = csv.reader(f)
            headers = next(r, None)  # skip header
            for row in r:
                # expecting 7 numeric columns: x,y,z,cx,cy,cz,t
                vals = list(map(float, row))
                if len(vals) < 7:
                    raise ValueError("Each row must have at least 7 numbers: x y z cx cy cz t")
                rows.append(Knot(*vals[:7]))
                
        return rows

    @staticmethod
    def _cubic(p0, c0, c1, p1, t):
        u = 1.0 - t

        return (u*u*u)*p0 + 3*(u*u)*t*c0 + 3*u*(t*t)*(2* p1 - c1) + (t*t*t)*p1

    def _segment_index(self, t: float) -> int:
        i = bisect.bisect_right(self.times, t) - 1

        return max(0, min(i, len(self.times) - 2))

    def point(self, t: float):
        i = self._segment_index(t)
        a = self.knots[i]
        b = self.knots[i + 1]
        
        tau = (t - a.t) / (b.t - a.t) if b.t != a.t else 0.0

        x = self._cubic(a.x, a.cx, b.cx, b.x, tau)
        y = self._cubic(a.y, a.cy, b.cy, b.y, tau)
        z = self._cubic(a.z, a.cz, b.cz, b.z, tau)
        return x, y, z