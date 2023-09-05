import sys

from pathlib import Path

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.models.virtual_robot import VirtualRobot
from lib.data.plot import DataPlotter

rob = VirtualRobot(0.8,  # distance 2 m
                   1.5,  # max speed 1.5 m/s
                   3.0,  # accel 3 m/s2
                   2.0)  # decel 2 m/s2

t = 0  # beginning of events
delta_t = 1e-3  # sampling interval = 1ms

plotter = DataPlotter()

while rob.phase != rob.TARGET:
    plotter.add('t', t)
    plotter.add('v', rob.v)
    plotter.add('p', rob.p)
    rob.evaluate(delta_t)
    t = t + delta_t

plotter.plot(['t', 'time'], [['v', 'Speed'],
                             ['p', 'Position']])
plotter.show()
