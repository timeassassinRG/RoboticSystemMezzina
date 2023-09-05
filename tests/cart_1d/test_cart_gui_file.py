#
# test_cart_gui_file.py
#

import sys

from pathlib import Path

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.models.cart import Cart
from lib.models.robot import RoboticSystem
from lib.gui.gui_1d import *
from lib.data.readers import *

from PyQt5.QtWidgets import QApplication


class CartSystem(RoboticSystem):

    def __init__(self, filename):
        super().__init__(1e-3)  # delta_t = 1e-3
        # Mass = 1kg
        # friction = 0.8
        self.cart = Cart(1, 0.8)
        self.datafile = FileReader(filename)
        self.datafile.load()

    def run(self):
        [F] = self.datafile.get_vars(self.t, ['F'])
        self.cart.evaluate(self.delta_t, F)
        return True

    def get_pose(self):
        return self.cart.position

    def get_speed(self):
        return self.cart.speed


if __name__ == '__main__':
    cart_sys = CartSystem(sys.argv[1])
    app = QApplication(sys.argv)
    ex = CartWindow(cart_sys)
    sys.exit(app.exec_())
