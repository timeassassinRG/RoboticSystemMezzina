#pragma once

#include <string>

#include <gazebo/common/common.hh>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/transport/transport.hh>

namespace gazebo
{

  class Pose : public ModelPlugin {
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

      //  Pointer to the world update function.
      event::ConnectionPtr updateConn;

      float lastTime;

  };

}
