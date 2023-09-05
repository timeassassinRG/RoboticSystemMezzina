/*
 * control_plugin.cc
 */

#include "control_plugin.h"

using namespace gazebo;

GZ_REGISTER_MODEL_PLUGIN(RobotControl)

void RobotControl::Load(physics::ModelPtr model, sdf::ElementPtr sdf) {
  this->model = model;

  // Parse SDF properties
  left_joint = model->GetJoint("left_wheel_hinge");
  right_joint = model->GetJoint("right_wheel_hinge");

  lastTime = 0;

  target_pos = new ignition::math::Vector3d(5, 8, 0);

  distance_pid = new PID(10, 0.0, 0.0, 10);
  heading_pid = new PID(5, 0.0, 0.0, 10);

  // Connect to the world update event.
  // This will trigger the Update function every Gazebo iteration
  updateConn = event::Events::ConnectWorldUpdateBegin(boost::bind(&RobotControl::Update, this, _1));
}

void RobotControl::Update(const common::UpdateInfo& info)
{
    float curr_time = model->GetWorld()->RealTime().Float();
    float delta_t = curr_time - lastTime;

    // apply control algorithm after 5 seconds
    if (curr_time > 5) {

        // start the control after 5 seconds of simulation

        float sleft = left_joint->GetVelocity(0);
        float sright = right_joint->GetVelocity(0);

        float current_linear_vel = model->RelativeLinearVel()[0]; // x axis
        float current_angular_vel = model->RelativeAngularVel()[2]; // z axis

        float current_heading = model->WorldPose().Yaw();

        ignition::math::Vector3d current_pos = model->WorldPose().Pos();
        current_pos.Z(0); // set the z = 0 in order to determine the distance

        float distance = current_pos.Distance(*target_pos);
        float target_heading = atan2(target_pos->Y() - current_pos.Y(),
                                     target_pos->X() - current_pos.X());

        float v_target = 0;
        float w_target = 0;

        if (distance > 0.1) {

            if (target_heading > M_PI/2) {
                target_heading = target_heading - M_PI;
                distance = -distance;
            }
            else if (target_heading < -M_PI/2) {
                target_heading = target_heading + M_PI;
                distance = -distance;
            }

            v_target = distance_pid->evaluate(delta_t, distance, 0);

            w_target = heading_pid->evaluate(delta_t, target_heading, current_heading);

        }

        left_joint->SetVelocity(0, v_target - w_target / 0.4);
        right_joint->SetVelocity(0, v_target + w_target / 0.4);

        gzmsg << "T:" << curr_time << "," << model->WorldPose() << std::endl;

        // gzmsg << "Time : " << curr_time <<
        //     " - Speed : " << sleft << "," << sright << " - " << linear_vel << "," << angular_vel << std::endl;
    }
    lastTime = curr_time;
}
