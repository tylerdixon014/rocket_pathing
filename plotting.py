import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from silly_billy_math import BezierSpline

spline = BezierSpline("sample.csv")

t0, t1 = spline.times[0], spline.times[-1]
ts = np.linspace(t0, t1, 300)

pts = [spline.point(t) for t in ts]
xs, ys, zs = zip(*pts)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(xs, ys, zs)
plt.show()