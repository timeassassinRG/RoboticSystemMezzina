import sys

from pathlib import Path

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.data.plot import DataPlotter


class MySystem:

    def __init__(self):
        self.x1 = 0
        self.x2 = 0

    def evaluate(self, delta_t, u):
        x1_temp = self.x1 + self.x2 * delta_t + 3 * delta_t * u
        x2_temp = self.x2 - 2 * delta_t * self.x1 + 1 * delta_t * self.x2
        y = self.x1
        self.x1 = x1_temp
        self.x2 = x2_temp
        return y


t = 0  # beginning of events
delta_t = 1e-3  # sampling interval = 1ms

_input = 3  # constant input

mysys = MySystem()
plotter = DataPlotter()

while t < 20:  # let's simulate 10 seconds
    y = mysys.evaluate(delta_t, _input)
    plotter.add('t', t)
    plotter.add('y', y)
    t = t + delta_t

plotter.plot(['t', 'Time'], [['y', 'Output']])
plotter.show()
