from matplotlib import pylab
import numpy as np


class KalmanFilter:

    def __init__(self, delta_t):
        # state vector x y vx vy, initial state to 0
        self.x = np.matrix([0, 0, 0, 0]).transpose()
        # process matrix
        self.A = np.matrix([[1, 0, delta_t, 0],  # x = x + delta_t * vx
                            [0, 1, 0, delta_t],  # y = y + delta_t * vy
                            [0, 0, 1, 0],  # vx = vx
                            [0, 0, 0, 1]])  # vy = vy

        # process covariance
        self.Q = np.eye(4, 4) * 0.05

        # measure covariance (initially high)
        self.R = np.eye(4, 4) * 10

        # measure matrix (only x and y masured)
        self.H = np.matrix([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]])
        # error covariance matrix
        self.P = np.matrix([[0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]])
        # Prediction
        self.K = None

    def prediction(self):
        self.x = self.A * self.x
        self.P = self.A * self.P * self.A.transpose() + self.Q  # prediction of
        S = self.H * self.P * self.H.transpose() + self.R
        self.K = (self.P * self.H.transpose()) * S.I

    def measure(self, measures):
        measures = np.matrix(measures).transpose()
        self.x = self.x + self.K * (measures - self.H * self.x)

    def update(self):
        self.P = (np.eye(4, 4) - self.K * self.H) * self.P


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
mean = 0.0

while t < 15:
    x = x + vx * delta_t
    y = y + vy * delta_t

    trajectory_x.append(x)
    trajectory_y.append(y)

    measure_x.append(x + np.random.normal(mean, error_std))
    measure_y.append(y + np.random.normal(mean, error_std))

    t = t + delta_t

t = 0

predicted_trajectory_x = []
predicted_trajectory_y = []

f = KalmanFilter(delta_t)
i = 0

while t < 15:
    f.prediction()
    f.measure([measure_x[i], measure_y[i], 0, 0])
    f.update()

    predicted_trajectory_x.append(f.x.A[0][0])
    predicted_trajectory_y.append(f.x.A[1][0])

    t = t + delta_t
    i = i + 1

pylab.figure(1)
pylab.plot(measure_x, measure_y, 'b-+', label='masures')
pylab.plot(trajectory_x, trajectory_y, 'r-+', label='real trajectory')
pylab.xlabel('x')
pylab.ylabel('y')
pylab.legend()

pylab.figure(2)
pylab.plot(trajectory_x, trajectory_y, 'r-+', label='real trajectory')
pylab.plot(predicted_trajectory_x, predicted_trajectory_y, 'g-+', label='fitered')
pylab.xlabel('x')
pylab.ylabel('y')
pylab.legend()

pylab.show()
