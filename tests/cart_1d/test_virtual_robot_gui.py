import sys

from pathlib import Path
from PyQt5.QtWidgets import QApplication

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.models.cart import Cart
from lib.models.robot import RoboticSystem
from lib.models.virtual_robot import VirtualRobot
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
        self.trajectory = VirtualRobot(8,  # distance 8 m
                                       1.5,  # max speed 1.5 m/s
                                       1.0,  # accel 1 m/s2
                                       1.0)  # decel 1 m/s2
        self.speed_controller = PIDSat(10.0, 8.0, 0.0, 2.0, True)  # Kp = 3, KI = 2, Sat = 2 N
        self.position_controller = PIDSat(4.0, 0.0, 0.8, 1.5)  # Kp = 8.0, Kd = 0.8, vmax = 1.5 m/s

    def run(self):
        self.trajectory.evaluate(self.delta_t)
        v_target = self.position_controller.evaluate(self.delta_t, self.trajectory.p, self.get_pose())
        F = self.speed_controller.evaluate(self.delta_t, v_target, self.get_speed())
        self.cart.evaluate(self.delta_t, F)
        self.plotter.add('t', self.t)
        self.plotter.add('virt_robot_speed', self.trajectory.v)
        self.plotter.add('target_speed', v_target)
        self.plotter.add('speed', self.get_speed())
        self.plotter.add('target_pos', self.trajectory.p)
        self.plotter.add('pos', self.get_pose())
        if self.t >= 10:
            self.plotter.plot(['t', 'time'], [['target_speed', 'Target Speed'],
                                              ['speed', 'Current Speed'],
                                              ['virt_robot_speed', 'Virtual Robot Speed']])
            self.plotter.plot(['t', 'time'], [['target_pos', 'Target Position'],
                                              ['pos', 'Current Position']])
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
