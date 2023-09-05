#pragma once

#include <string>

#include <gazebo/common/common.hh>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/transport/transport.hh>

#include "pid.h"

namespace gazebo
{

  class RobotControl : public ModelPlugin {
    public:
    // Load the dc motor and configures it according to the sdf.
    void Load(physics::ModelPtr model, sdf::ElementPtr sdf);

    // Update the torque on the joint from the dc motor each timestep.
    void Update(const common::UpdateInfo& info);

    private:
      // Topic to write encoder signals to.
      std::string topic;

      // The model to which this is attached.
      physics::ModelPtr model;
      physics::JointPtr left_joint;
      physics::JointPtr right_joint;

      //  Pointer to the world update function.
      event::ConnectionPtr updateConn;

      float lastTime;

      PID * heading_pid, * distance_pid;
      ignition::math::Vector3d * target_pos;
  };

}
