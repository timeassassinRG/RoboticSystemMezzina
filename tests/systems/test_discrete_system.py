import sys
import numpy as np

from pathlib import Path

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.data.plot import DataPlotter


class MyDiscreteSystem:

    def __init__(self, A, B, C, delta_t):
        size = len(A)
        self.A_t = np.array(A) * delta_t + np.eye(size, size)
        self.B_t = np.array(B) * delta_t
        self.C_t = np.array(C)
        self.x = np.zeros((size, 1))

    def evaluate(self, delta_t, u):
        output = self.C_t @ self.x
        self.x = self.A_t @ self.x + self.B_t * u
        return output[0]


t = 0  # beginning of events
delta_t = 1e-3  # sampling interval = 1ms

_input = 3  # constant input

A = [[0, 1],
     [-3, -2]]

B = [[3],
     [0]]

C = [1, 0]

mysys = MyDiscreteSystem(A, B, C, delta_t)
plotter = DataPlotter()

while t < 20:  # let's simulate 10 seconds
    y = mysys.evaluate(delta_t, _input)
    plotter.add('t', t)
    plotter.add('y', y)
    t = t + delta_t

plotter.plot(['t', 'Time'], [['y', 'Output']])
plotter.show()
