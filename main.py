from plotting import plot

filepath = "sample.csv"
sensor = [0.1,0.1,0.125]
sample_count = 1000

# To get just the numbers:
# Initialize a spline with spline = Spline(filepath)
# You can get center of mass at time t via spline.evaluate(t)
# For a sensor at [x,y,z] (relative to the center of mass), the position at time t is spline.sensor(sensor, t)

plot(filepath, sensor, sample_count)