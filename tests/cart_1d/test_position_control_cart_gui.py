import sys

from pathlib import Path
from PyQt5.QtWidgets import QApplication

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.models.cart import Cart
from lib.models.robot import RoboticSystem
from lib.controllers.standard import Proportional
from lib.gui.gui_1d import CartWindow


class CartRobot(RoboticSystem):

    def __init__(self):
        super().__init__(1e-3)  # delta_t = 1e-3
        # Mass = 1kg
        # friction = 0.8
        self.cart = Cart(1, 0.8)
        self.controller = Proportional(0.2)  # Kp = 0.2
        self.target_position = 4  # 4 meters

    def run(self):
        F = self.controller.evaluate(self.target_position, self.get_pose())
        self.cart.evaluate(self.delta_t, F)
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
