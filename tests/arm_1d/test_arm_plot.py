import sys
import math

from pathlib import Path
from matplotlib import pylab

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.models.arm import Arm

arm = Arm(1, 0.8, 0.6)  # mass 1 Kg, friction = 0.8, r = 0.6 (60cm)

t = 0  # beginning of events
delta_t = 1e-3  # sampling interval = 1ms

_input = 3  # constant input of 3 Nm

time_array = []
speed_array = []
position_array = []

while t < 20:  # let's simulate 20 seconds
    time_array.append(t)
    speed_array.append(arm.omega)
    position_array.append(math.degrees(arm.theta))
    arm.evaluate(delta_t, _input)
    t = t + delta_t

pylab.figure(1)
pylab.plot(time_array, speed_array, 'r-', label='speed, omega(t)')
pylab.xlabel('time')
pylab.legend()

pylab.figure(2)
pylab.plot(time_array, position_array, 'r-', label='position, theta(t)')
pylab.xlabel('time')
pylab.legend()

pylab.show()
