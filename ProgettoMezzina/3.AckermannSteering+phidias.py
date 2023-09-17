from pathlib import Path
import sys
CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/..")
import numpy as np
import math
from matplotlib import pylab
from PyQt5.QtWidgets import QApplication
from lib.gui.gui_2d import CartWindow
from lib.models.cart2d import AckermannSteering
from lib.models.robot import RoboticSystem
from lib.controllers.standard import PIDSat
from lib.controllers.control2d import Polar2DController, StraightLine2DMotion, Path2D
from lib.gui.gui_2d import CartWindow
from lib.data.plot import DataPlotter
from lib.phidias.phidias_interface import start_message_server_http, Messaging
import PathPlanning as PATH_PLANNER

#definizione delle costanti fornite dal testo del progetto
MASS = 15               # Massa del robot = 15kg
SLIDE = 0.2             # Largezza del robot = 20cm
WHEEL_RADIUS = 0.03     # Raggio delle ruote = 3cm
FRICTION = 0.7          # Coefficiente di attrito viscoso, 0.7;
TORQUE_MAX = 20         # Coppia massima = 20Nm
V_MAX = 0.2            # Velocità massima = 2m/s   
ACC = 1.5                 # Accelerazione massima = 1.5m/s^2  (a piacere)
DEC = 1.5                 # Decelerazione massima = 2.5m/s^2  (a piacere)

class AckermannRobot(RoboticSystem):
    def __init__(self):
        super().__init__(1e-3) # delta_t = 1e-3
        self.car = AckermannSteering(MASS, FRICTION, WHEEL_RADIUS, SLIDE)

        # 20Nm of max torque, antiwindup
        self.speed_controller = PIDSat(80, 10, 0, TORQUE_MAX, True)

        # Path controller
        self.polar_controller = Polar2DController(2.0, V_MAX, 10.0, math.pi/3)
        self.path_controller = Path2D(V_MAX, ACC, DEC, 0.05)
        self.path_controller.set_path( [ (0, 0)] )
        (x,y,_) = self.get_pose()
        self.path_controller.start( (x,y) )
        self.target_reached = False

        #networking
        self.phidias_agent = ''
        start_message_server_http(self)
        self.obstacle_points = ([(0.25, 0.35), (0.4, 0.05), (0.55, 0.25), (0.82, 0.15), (0.80, 0.35)])  # Lista per memorizzare i punti degli ostacoli
        self.path_planner = PATH_PLANNER.PathPlanning((x, y), self.obstacle_points)
        
  
    def set_obstacle_points(self, obstacle_points):
        self.obstacle_points = obstacle_points

    def run(self):
        pose = self.get_pose()
        target = self.path_controller.evaluate(self.delta_t, pose)
        if target is not None:
            (x_target, y_target) = target
            (vref, steering) = self.polar_controller.evaluate(self.delta_t, x_target, y_target, self.get_pose())
            if vref < 0:
                steering = -steering
            torque = self.speed_controller.evaluate(self.delta_t, vref, self.car.v)
            self.car.evaluate(self.delta_t, torque, steering)
        else:
            if not self.target_reached:
                self.target_reached = True
                if self.phidias_agent != '':
                    print("ROBOT >> path planner reached checkpoint: ", self.path_planner.checkpoints[0])
                    print("ROBOT >> path planner deleting checkpoint: ", self.path_planner.checkpoints[0])
                    self.path_planner.reached_checkpoint()
                    print('ROBOT >> Target reached, sending message to phidias agent')
                    Messaging.send_belief(self.phidias_agent, 'target_reached', [], 'robot')
                    self.path_planner.clear_goals()
        return True
    
    def get_pose(self):
        return self.car.get_pose()

    def get_speed(self):
        return self.car.v, self.car.w
    
    def on_belief(self, _from, name, terms):
        print(_from, name, terms)
        self.phidias_agent = _from
        if name == 'go_to':
            self.path_planner.add_goal(np.array([float(terms[0]), float(terms[1])]))
            self.path_planner._update_graph()
            path = self.path_planner.find_path()
            print(path)
            self.path_controller.set_path(path)
            (x,y,_) = self.get_pose()
            self.path_controller.start( (x,y) )
            self.target_reached = False
        if name == 'add_to':
            self.path_planner.add_goal(np.array([float(terms[0]), float(terms[1])]))
            self.path_planner._update_graph()
            print("ROBOT >> Aggiunto (", float(terms[0]), ",", float(terms[1]), ") alla coda di target.")
        if name == 'clear_path':
            self.path_planner.clear_goals()
            print("ROBOT >> Percorso cancellato.")
    
if __name__ == '__main__':
    cart_robot = AckermannRobot()
    app = QApplication(sys.argv)
    ex = CartWindow(cart_robot, 'ackermann_robot_2d.png')
    sys.exit(app.exec_())