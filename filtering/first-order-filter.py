from matplotlib import pylab
import numpy as np


class LowPassFilter:

    def __init__(self, alpha):
        self.alpha = alpha
        self.y = 0

    def evaluate(self, measure):
        self.y = self.y * (1 - self.alpha) + measure * self.alpha
        return self.y


delta_t = 1e-3  # 1 ms

vx = 0.5  # pix/s
vy = 0.8  # pix/s

t = 0.0

trajectory_x = []
trajectory_y = []

measure_x = []
measure_y = []

x = 0
y = 0

error_std = 0.05

N = 0
max_T = 5

while t < max_T:
    x = x + vx * delta_t
    y = y + vy * delta_t

    trajectory_x.append(x)
    trajectory_y.append(y)

    measure_x.append(x + np.random.normal(0.0, error_std))
    measure_y.append(y + np.random.normal(0.0, error_std))

    t = t + delta_t
    N = N + 1

t = 0

filtered_trajectory_x = []
filtered_trajectory_y = []

Alpha = 0.05

fx = LowPassFilter(Alpha)
fy = LowPassFilter(Alpha)

i = 0

while t < max_T:
    filtered_trajectory_x.append(fx.evaluate(measure_x[i]))
    filtered_trajectory_y.append(fy.evaluate(measure_y[i]))

    t = t + delta_t
    i = i + 1

pylab.figure(1)
pylab.plot(measure_x, measure_y, 'b-+', label='measures')
pylab.plot(trajectory_x, trajectory_y, 'r-+', label='real trajectory')
pylab.xlabel('x')
pylab.ylabel('y')
pylab.legend()

pylab.figure(2)
pylab.plot(filtered_trajectory_x, filtered_trajectory_y, 'g-+', label='fitered')
pylab.plot(trajectory_x, trajectory_y, 'r-+', label='real trajectory')
pylab.xlabel('x')
pylab.ylabel('y')
pylab.legend()

pylab.show()
