import sys
import math

from pathlib import Path
from PyQt5.QtWidgets import QApplication

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.models.arm import Arm
from lib.models.robot import RoboticSystem
from lib.gui.gui_1d import ArmWindow
from lib.data.plot import DataPlotter


class ArmRobot(RoboticSystem):

    def __init__(self):
        super().__init__(1e-3)  # delta_t = 1e-3
        # Mass = 1kg
        # friction = 0.8
        # lenght = 0.6
        self.arm = Arm(1, 0.8, 0.6)
        self.plotter = DataPlotter()

    def run(self):
        T = 3  # 3 Nm
        self.arm.evaluate_no_approx(self.delta_t, T)
        # self.arm.evaluate(self.delta_t, T)
        self.plotter.add('t', self.t)
        self.plotter.add('T', T)
        self.plotter.add('omega', self.get_speed())
        self.plotter.add('theta', math.degrees(self.get_pose()))
        if self.t >= 20:  # after 20 seconds plot data and stop simulation
            self.plotter.plot(['t', 'time'],
                              [['omega', 'Speed']])
            self.plotter.plot(['t', 'time'],
                              [['theta', 'Position']])
            self.plotter.show()
            return False
        else:
            return True

    def get_pose(self):
        return self.arm.theta

    def get_speed(self):
        return self.arm.omega


if __name__ == '__main__':
    cart_sys = ArmRobot()
    app = QApplication(sys.argv)
    ex = ArmWindow(cart_sys)
    sys.exit(app.exec_())
