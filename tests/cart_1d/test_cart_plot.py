import sys

from pathlib import Path
from matplotlib import pylab

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.models.cart import Cart

cart = Cart(1, 0.8)  # mass 1 Kg, friction = 0.8

t = 0  # beginning of events
delta_t = 1e-3  # sampling interval = 1ms

_input = 3  # constant input of 3 N

time_array = []
speed_array = []
position_array = []

while t < 10:  # let's simulate 10 seconds
    time_array.append(t)
    speed_array.append(cart.speed)
    position_array.append(cart.position)
    cart.evaluate(delta_t, _input)
    t = t + delta_t

pylab.figure(1)
pylab.plot(time_array, speed_array, 'r-+', label='speed, v(t)')
pylab.xlabel('time')
pylab.legend()

pylab.figure(2)
pylab.plot(time_array, position_array, 'r-+', label='position, p(t)')
pylab.xlabel('time')
pylab.legend()

pylab.show()
