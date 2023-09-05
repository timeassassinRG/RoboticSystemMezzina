import pylab

class Cart:
    def __init__(self, M, b):   # b = friction, M = mass
        self.b = b
        self.M = M
        self.speed = 0.0    # si suppone che si parta da uno stato di quiete

    def evaluate(self, _input, delta_t): #input = f all'istante t
        self.speed = self.speed - (self.b/self.M)*delta_t*self.speed \
                                + (delta_t/self.M)*_input
        return self.speed

# main 
if __name__ == "__main__":
    cart = Cart(25.0, 6.0) # M = 25kg, b = 6N*s/m
    t = 0
    delta_t = 1e-3 # 1ms
    f = 5 # 5N constant force
    speed_array = []
    time_array = []

    while t < 20:
        speed = cart.evaluate(f, delta_t)
        
        speed_array.append(speed)
        time_array.append(t)

        t = t + delta_t

pylab.figure(1)
pylab.plot(time_array, speed_array)
pylab.xlabel('Time [s]')
pylab.ylabel('Speed [m/s]')
pylab.show()