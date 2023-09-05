import sys

from pathlib import Path
from PyQt5.QtWidgets import QApplication

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.models.cart import Cart
from lib.models.robot import RoboticSystem
from lib.controllers.standard import PIDSat, PID
from lib.data.plot import DataPlotter
from lib.gui.gui_1d import CartWindow


class CartRobot(RoboticSystem):

    def __init__(self):
        super().__init__(1e-3)  # delta_t = 1e-3
        # Mass = 1kg
        # friction = 0.8
        self.cart = Cart(1, 0.8)
        self.plotter = DataPlotter()
        self.controller = PIDSat(6.0, 6.0, 0.0, 2.0, True)  # Kp = 3, KI = 2, Sat = 2 N
        # self.controller = PID(3.0, 2.0, 0.0) # Kp = 3, KI = 2
        self.target_speed = 1.5  # 1.5 m/s

    def run(self):
        F = self.controller.evaluate(self.delta_t, self.target_speed, self.get_speed())
        self.cart.evaluate(self.delta_t, F)
        self.plotter.add('t', self.t)
        self.plotter.add('target', self.target_speed)
        self.plotter.add('speed', self.get_speed())
        self.plotter.add('F', F)
        if self.t >= 15:
            self.plotter.plot(['t', 'time'], [['target', 'Target'],
                                              ['speed', 'Current Speed'],
                                              ['F', 'Force']])
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
