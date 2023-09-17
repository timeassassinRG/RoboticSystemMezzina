import sys
import math

from pathlib import Path

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/..")

from lib.models.cart2d import TwoWheelsCart2D
from lib.models.robot import RoboticSystem
from lib.controllers.standard import PIDSat
from lib.data.plot import DataPlotter
from lib.gui.gui_2d import CartWindow

from PyQt5.QtWidgets import QApplication


class Cart2DRobot(RoboticSystem):

    def __init__(self):
        super().__init__(1e-3)  # delta_t = 1e-3
        self.cart = TwoWheelsCart2D(20, 0.15, 0.8, 0.8,
                                                    0.025, 0.025, 0.2,
                                                    0.02, 0.02, 0.24, 2 * math.pi / 4000.0)
        self.plotter = DataPlotter()


        # 5 Nm of max torque, antiwindup
        self.left_controller = PIDSat(8.0, 3.0, 0.0, 5, True)
        self.right_controller = PIDSat(8.0, 3.0, 0.0, 5, True)

    def run(self):

        v_ref = 0.05
        w_ref = 0.5

        vref_l = v_ref - w_ref * self.cart.encoder_wheelbase / 2.0
        vref_r = v_ref + w_ref * self.cart.encoder_wheelbase / 2.0

        (vl, vr) = self.cart.get_wheel_speed()

        Tleft = self.left_controller.evaluate(self.delta_t, vref_l, vl)
        Tright = self.right_controller.evaluate(self.delta_t, vref_r, vr)

        self.cart.evaluate(self.delta_t, Tleft, Tright)

        self.plotter.add( 't', self.t)
        self.plotter.add( 'vl', vl)
        self.plotter.add( 'vr', vr)
        self.plotter.add( 'vref_l', vref_l)
        self.plotter.add( 'vref_r', vref_r)
        if self.t > 5:
            self.plotter.plot( ['t', 'time'] , [ [ 'vref_l', 'Vref' ],
                                                 [ 'vl', 'VL' ] ])
            self.plotter.plot( ['t', 'time'] , [ [ 'vref_r', 'Vref' ],
                                                 [ 'vr', 'VR' ] ])
            self.plotter.show()
            return False
        else:
            return True

    def get_pose(self):
        return self.cart.get_pose()

    def get_speed(self):
        return self.cart.get_speed()


if __name__ == '__main__':
    cart_robot = Cart2DRobot()
    app = QApplication(sys.argv)
    ex = CartWindow(cart_robot)
    sys.exit(app.exec_())
