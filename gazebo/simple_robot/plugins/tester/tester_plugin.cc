#include "tester_plugin.h"

using namespace gazebo;

GZ_REGISTER_MODEL_PLUGIN(Tester)

void Tester::Load(physics::ModelPtr model, sdf::ElementPtr sdf) {
  this->model = model;

  // Parse SDF properties
  left_joint = model->GetJoint("left_wheel_hinge");
  right_joint = model->GetJoint("right_wheel_hinge");

  // topic = "~/encoders";

  // gzmsg << "Initializing encoders: " << topic
  //       << " left_joint=" << left_joint->GetName()
  //       << " right_joint=" << right_joint->GetName() << std::endl;

  // // Connect to Gazebo transport for messaging
  // node = transport::NodePtr(new transport::Node());
  // node->Init(model->GetWorld()->GetName());
  // pub = node->Advertise<msgs::EncoderMsg>(topic);

  // left_joint->SetVelocity(0, 10);
  // right_joint->SetVelocity(0, 10);
  left_joint->SetForce(0, 30);
  right_joint->SetForce(0, 30);

  // Connect to the world update event.
  // This will trigger the Update function every Gazebo iteration
  updateConn = event::Events::ConnectWorldUpdateBegin(boost::bind(&Tester::Update, this, _1));
}

void Tester::Update(const common::UpdateInfo& info) {
    // gzmsg << "Time : " << model->GetWorld()->RealTime().Float() << std::endl;
    // gzmsg << "Pose : " << model->WorldPose() << std::endl;

  // msgs::EncoderMsg msg;
  // msg.set_timestamp(model->GetWorld()->GetSimTime().Float());
  // msg.set_left_angle(left_joint->GetAngle(0).Radian());
  // msg.set_right_angle(right_joint->GetAngle(0).Radian());
  // msg.set_left_velocity(left_joint->GetVelocity(0));
  // msg.set_right_velocity(right_joint->GetVelocity(0));

  // pub->Publish(msg);
}
