from pathlib import Path
import sys
CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/..")
import math
from matplotlib import pylab
from PyQt5.QtWidgets import QApplication
from lib.gui.gui_2d import CartWindow
from lib.models.cart2d import AckermannSteering
from lib.models.robot import RoboticSystem
from lib.controllers.standard import PIDSat
from lib.controllers.control2d import Polar2DController, StraightLine2DMotion, Path2D
from lib.gui.gui_2d_Original import CartWindow
from lib.data.plot import DataPlotter

#definizione delle costanti fornite dal testo del progetto
MASS = 15.0             # Massa del robot = 15kg
SLIDE = 0.2             # Largezza del robot = 20cm
WHEEL_RADIUS = 0.03     # Raggio delle ruote = 3cm
FRICTION = 0.7          # Coefficiente di attrito viscoso, 0.7;
TORQUE_MAX = 20.0         # Coppia massima = 20Nm
V_MAX = 0.2            # Velocità massima = 2m/s   
ACC = 1.5                 # Accelerazione massima = 1.5m/s^2  (a piacere)
DEC = 1.5                 # Decelerazione massima = 2.5m/s^2  (a piacere)

_THRESHOLD = 0.001 # per ottenere dei grafici migliori, nella pratica ho usato 0.05

class AckermannRobot(RoboticSystem):
    def __init__(self):
        super().__init__(1e-3) # delta_t = 1e-3
        self.car = AckermannSteering(MASS, FRICTION, WHEEL_RADIUS, SLIDE)
        (self.car.x, self.car.y) = (0,0)
        # aggiungiamo il percorso
        self.path_controller = Path2D(V_MAX, ACC, DEC, _THRESHOLD)
        # aggiungiamo controller di posizione
        self.polar_controller = Polar2DController(2.0, V_MAX, 12.0, math.pi/3)
        # aggiungiamo controller di velocità 20 Nm max, antiwindup
        self.speed_controller = PIDSat(80, 10, 0, TORQUE_MAX, False)
        
        self.path_controller.set_path( [ (0.25, 0.1), (0.40, 0.25), (0.65, 0.30)] )
        (x,y,_) = self.get_pose()
        self.path_controller.start( (x,y) )
        self.plotter = DataPlotter()
    
    def run(self):
        target = self.path_controller.evaluate(self.delta_t, self.get_pose())
        if target is not None:
            (x_target, y_target) = target
            (vref, steering) = self.polar_controller.evaluate(self.delta_t, x_target, y_target, self.get_pose())
            if vref < 0:
                steering = -steering
            torque = self.speed_controller.evaluate(self.delta_t, vref, self.car.v)
            self.car.evaluate(self.delta_t, torque, steering)
        else:
            self.plot_data()
            return False
        
        (x,y,_) = self.get_pose()
        self.plotter.add('t', self.t)
        self.plotter.add('x_target', x_target)
        self.plotter.add('y_target', y_target)
        self.plotter.add('x', x)
        self.plotter.add('y', y)
        self.plotter.add('Torque', torque)
        self.plotter.add('TorqueMax', TORQUE_MAX)
        self.plotter.add('vref', vref)
        self.plotter.add('v', self.car.v)
    
        if self.t > 10:
            self.plot_data()
            return False
        return True
    
    def plot_data(self):
        #ploot x target and x position
            self.plotter.plot ( [ 't', 'Time' ], [ [ 'x', 'X' ],
                                                   [ 'x_target', 'X Target']])
            #plot y target and y position
            self.plotter.plot ( [ 't', 'Time' ], [ [ 'y', 'Y' ],
                                                   [ 'y_target', 'Y Target']])
            
            #plot xtarget and ytarget and actual x and y
            self.plotter.plot ( [ 't', 'Time' ], [ [ 'Torque', 'Torque'], ['TorqueMax','TorqueMax'] ])
            self.plotter.plot ( [ 't', 'Time' ], [ [ 'v', 'V' ],
                                                   [ 'vref', 'Vref'] ])
            self.plotter.show()  
            return False
           
    def get_pose(self):
        return self.car.get_pose()

    def get_speed(self):
        return self.car.v, self.car.w
    
    
if __name__ == '__main__':
    cart_robot = AckermannRobot()
    app = QApplication(sys.argv)
    ex = CartWindow(cart_robot, 'ackermann_robot_2d.png')
    sys.exit(app.exec_())