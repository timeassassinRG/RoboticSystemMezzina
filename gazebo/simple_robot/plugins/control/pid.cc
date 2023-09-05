/*
 * pid.cc
 */

#include "pid.h"

PID::PID(float _kp, float _ki, float _kd, float _saturation) :
    kp(_kp), ki(_ki), kd(_kd), saturation(_saturation),
    integral(0), in_saturation(false), prev_error(0)
{
}

float PID::evaluate(float delta_t, float target, float current)
{
    float error = target - current;

    if (!in_saturation)
        integral = integral + error * delta_t;

    float output = kp * error + ki * integral + kd * (error - prev_error) / delta_t;

    if (output > saturation) {
        output = saturation;
        in_saturation = true;
    }
    else if (output < - saturation) {
        output = - saturation;
        in_saturation = true;
    }
    else
        in_saturation = false;

    return output;
}

