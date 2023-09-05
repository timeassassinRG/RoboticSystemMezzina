import sys

from pathlib import Path

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.models.multirotor import Multirotor2D
from lib.models.robot import RoboticSystem
from lib.gui.multirotor_gui import MultirotorWindow

from PyQt5.QtWidgets import QApplication


class MultirotorRobot(RoboticSystem):

    def __init__(self):
        super().__init__(1e-3)  # delta_t = 1e-3
        self.MR = Multirotor2D(1.0, 0.25)  # 1.0kg, L = 25cm

    def run(self):
        f1 = 5.0
        f2 = 5.0
        self.MR.evaluate(self.delta_t, f1, f2)
        return True

    def get_pose(self):
        return self.MR.x, self.MR.z, self.MR.theta

    def get_speed(self):
        return self.MR.vx, self.MR.vz, self.MR.omega


if __name__ == '__main__':
    robot = MultirotorRobot()
    app = QApplication(sys.argv)
    ex = MultirotorWindow(robot)
    sys.exit(app.exec_())
