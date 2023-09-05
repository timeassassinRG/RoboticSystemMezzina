import sys
from pathlib import Path
CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../")
import numpy as np
import matplotlib.pyplot as plt
from lib.data.plot import DataPlotter
from filtering.imu_driver import IMUDriver

drv = IMUDriver()
drv.open()
plot = DataPlotter()

for i in range(0, 1000):
    (ax, ay, az, gx, gy, gz) = drv.sample()
    plot.add('i', i)
    plot.add('gz', gz)

gz_array = plot.data['gz']
avg = np.mean(gz_array)
for i in range(0, 1000):
    plot.add('avg', avg)

plot.plot(['i', 'Samples'], [['gz', 'Gyro Z'], ['avg', 'Average']])
plot.show()

plt.hist(gz_array, bins=100, density=True, label="Histogram of samples")
plt.show()
