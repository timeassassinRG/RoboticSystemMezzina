/*
 * pid.h
 */

#pragma once

#include <stdbool.h>

class PID {
 public:
    PID(float _kp, float _ki, float _kd, float _saturation);
    float evaluate(float delta_t, float target, float current);
 private:
    float kp, ki, kd, saturation, integral;
    bool in_saturation;
    float prev_error;
};

