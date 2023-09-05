import sys
import math
from pathlib import Path
from PyQt5.QtWidgets import QApplication

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.models.cart2d import AckermannSteering
from lib.models.robot import RoboticSystem
from lib.gui.gui_2d import CartWindow


class AckermannRobot(RoboticSystem):

    def __init__(self):
        super().__init__(1e-3)  # delta_t = 1e-3
        # Mass = 10kg
        # side = 15cm
        # wheels radius = 2cm
        # friction = 0.8
        self.car = AckermannSteering(10, 0.8, 0.02, 0.15)

    def run(self):
        Torque = 0.02
        Steering = math.radians(10)

        self.car.evaluate(self.delta_t, Torque, Steering)
        return True

    def get_pose(self):
        return self.car.get_pose()

    def get_speed(self):
        return self.car.v, self.car.w


if __name__ == '__main__':
    cart_robot = AckermannRobot()
    app = QApplication(sys.argv)
    ex = CartWindow(cart_robot, 'ackermann_robot_2d.png')
    sys.exit(app.exec_())
