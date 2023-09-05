import time
import math

from imu_driver import IMUDriver
from comp_filter import ComplementaryAHRSFilter

imu = IMUDriver()

imu.open()

filt = ComplementaryAHRSFilter(1.0, 0.2)

last_t = time.time()

while True:
    imu_data = imu.sample()
    t = time.time()
    delta_t = t - last_t
    filt.update(delta_t,
                imu_data[0], imu_data[1], imu_data[2],
                imu_data[3], imu_data[4], imu_data[5])
    last_t = t
    (r, p) = filt.get_attitude()
    print(math.degrees(r), math.degrees(p))
