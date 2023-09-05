import sys

from pathlib import Path
from PyQt5.QtWidgets import QApplication

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.models.cart import Cart
from lib.models.robot import RoboticSystem
from lib.controllers.standard import PIDSat
from lib.data.plot import DataPlotter
from lib.gui.gui_1d import CartWindow


class CartRobot(RoboticSystem):

    def __init__(self):
        super().__init__(1e-3)  # delta_t = 1e-3
        # Mass = 1kg
        # friction = 0.8
        self.cart = Cart(1, 0.8)
        self.plotter = DataPlotter()
        self.controller = PIDSat(0.2, 0, 0, 0.5)  # Kp = 0.2, saturation 0.5 Newton
        # self.controller = PID(0.2, 0, 0) # Kp = 0.2
        self.target_position = 4  # 4 meters

    def run(self):
        F = self.controller.evaluate(self.delta_t, self.target_position, self.get_pose())
        self.cart.evaluate(self.delta_t, F)
        self.plotter.add('t', self.t)
        self.plotter.add('F', F)
        self.plotter.add('target', self.target_position)
        self.plotter.add('position', self.get_pose())
        if self.t >= 15:
            self.plotter.plot(['t', 'time'], [['target', 'Target'],
                                              ['position', 'Current Position'],
                                              ['F', 'Controller Output']])
            self.plotter.show()
            return False
        else:
            return True

    def get_pose(self):
        return self.cart.position

    def get_speed(self):
        return self.cart.speed


if __name__ == '__main__':
    cart_robot = CartRobot()
    app = QApplication(sys.argv)
    ex = CartWindow(cart_robot)
    sys.exit(app.exec_())
