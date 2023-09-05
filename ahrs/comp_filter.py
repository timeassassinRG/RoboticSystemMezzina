import math


class ComplementaryAHRSFilter:

    def __init__(self, kp, ki):
        self.q0 = 1
        self.q1 = 0
        self.q2 = 0
        self.q3 = 0
        self.kp = kp
        self.ki = ki
        self.K_dyn_correction = 50
        self.bias_x = 0
        self.bias_y = 0
        self.bias_z = 0

    def update(self, delta_t, ax, ay, az, gx, gy, gz):
        m_halfT = delta_t / 2.0
        gx = math.radians(gx)
        gy = math.radians(gy)
        gz = math.radians(gz)

        # normalize acceleration measurement
        a_norm = math.sqrt(ax * ax + ay * ay + az * az)
        ax = ax / a_norm
        ay = ay / a_norm
        az = az / a_norm

        # evaluate dynamic correction factor
        d = a_norm - 1
        err_g = math.exp(- (d * d) * self.K_dyn_correction)

        # estimate direction of gravity by rotating the vector (0, 0, 1)
        gravity_x = 2 * (self.q1 * self.q3 - self.q0 * self.q2)
        gravity_y = 2 * (self.q2 * self.q3 + self.q0 * self.q1)
        gravity_z = self.q0 * self.q0 - self.q1 * self.q1 - self.q2 * self.q2 + self.q3 * self.q3

        # calculate error using cross product between
        # reference direction of field and direction measured by sensor
        gravity_err_x = (ay * gravity_z - az * gravity_y) * err_g
        gravity_err_y = (az * gravity_x - ax * gravity_z) * err_g
        gravity_err_z = (ax * gravity_y - ay * gravity_x) * err_g

        # compute proportional correction
        ex = gravity_err_x * self.kp
        ey = gravity_err_y * self.kp
        ez = gravity_err_z * self.kp

        # compute integral correction
        self.bias_x = self.bias_x + gravity_err_x * self.ki
        self.bias_y = self.bias_y + gravity_err_y * self.ki
        self.bias_z = self.bias_z + gravity_err_z * self.ki

        # adjust gyroscope measurements
        gx = gx + ex + self.bias_x
        gy = gy + ey + self.bias_y
        gz = gz + ez + self.bias_z

        # integrate quaternion
        qa = self.q0 + (-self.q1 * gx - self.q2 * gy - self.q3 * gz) * m_halfT
        qb = self.q1 + (self.q0 * gx - self.q3 * gy + self.q2 * gz) * m_halfT
        qc = self.q2 + (self.q3 * gx + self.q0 * gy - self.q1 * gz) * m_halfT
        qd = self.q3 + (-self.q2 * gx + self.q1 * gy + self.q0 * gz) * m_halfT

        # normalise quaternion
        norm = math.sqrt(qa * qa + qb * qb + qc * qc + qd * qd)
        qa = qa / norm
        qb = qb / norm
        qc = qc / norm
        qd = qd / norm

        if (not (math.isnan(qa))) and (not (math.isnan(qb))) and (not (math.isnan(qc))) and (not (math.isnan(qd))):
            self.q0 = qa
            self.q1 = qb
            self.q2 = qc
            self.q3 = qd

    def get_attitude(self):
        roll = math.atan2(2 * (self.q0 * self.q1 + self.q2 * self.q3),
                          self.q0 * self.q0 - self.q1 * self.q1 - self.q2 * self.q2 + self.q3 * self.q3)
        pitch = math.asin(2 * (self.q0 * self.q2 - self.q1 * self.q3))

        return roll, pitch
