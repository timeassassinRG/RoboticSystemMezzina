from matplotlib import pylab
import numpy as np

delta_t = 1e-3  # 1 ms

vx = 0.5  # pix/s
vy = 0.8  # pix/s

t = 0.0

trajectory_x = []
trajectory_y = []

measure_x = []
measure_y = []

times = []

x = 0
y = 0

error_std = 0.05

N = 0

while t < 15:
    x = x + vx * delta_t
    y = y + vy * delta_t

    trajectory_x.append(x)
    trajectory_y.append(y)

    measure_x.append(x + np.random.normal(0.0, error_std))
    measure_y.append(y + np.random.normal(0.0, error_std))

    times.append(t)

    t = t + delta_t
    N = N + 1

pylab.figure(1)
pylab.plot(measure_x, measure_y, 'b-+', label='masures')
pylab.plot(trajectory_x, trajectory_y, 'r-+', label='real trajectory')
pylab.xlabel('x')
pylab.ylabel('y')
pylab.legend()

# pylab.figure(2)
# sp = np.fft.fft(measure_x)
# freq = np.fft.fftfreq(len(times))
# pylab.plot(freq, sp.real, freq, sp.imag)


pylab.show()
