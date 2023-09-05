import sys

from pathlib import Path
from PyQt5.QtWidgets import QApplication

CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../../")

from lib.models.cart2d import AckermannSteering
from lib.models.robot import RoboticSystem
from lib.models.inputs import RampSat
from lib.controllers.standard import PIDSat
from lib.data.plot import DataPlotter
from lib.gui.gui_2d import CartWindow


class AckermannRobot(RoboticSystem):

    def __init__(self):
        super().__init__(1e-3)  # delta_t = 1e-3
        # Mass = 10kg
        # side = 15cm
        # wheels radius = 2cm
        # friction = 0.8
        self.car = AckermannSteering(10, 0.8, 0.02, 0.15)
        # 5 Nm max, antiwindup
        self.speed_controller = PIDSat(8.0, 2.0, 0, 5, True)
        self.reference = RampSat(1.5, 2.0)  # acc = 1.5 m/s2, vamax = 2 m/s
        self.plotter = DataPlotter()

    def run(self):
        (v, w) = self.get_speed()
        vref = self.reference.evaluate(self.delta_t)

        Torque = self.speed_controller.evaluate(self.delta_t, vref, v)
        Steering = 0

        self.car.evaluate(self.delta_t, Torque, Steering)

        self.plotter.add('t', self.t)
        self.plotter.add('vref', vref)
        self.plotter.add('v', v)

        if self.t > 3:
            self.plotter.plot(['t', 'Time'], [['v', 'V'],
                                              ['vref', 'Vref']])
            self.plotter.show()
            return False
        else:
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
