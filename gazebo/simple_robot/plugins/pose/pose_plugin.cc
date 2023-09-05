#include "pose_plugin.h"

using namespace gazebo;

GZ_REGISTER_MODEL_PLUGIN(Pose)

void Pose::Load(physics::ModelPtr model, sdf::ElementPtr sdf)
{
    lastTime = 0;
    this->model = model;

    // Connect to the world update event.
    // This will trigger the Update function every Gazebo iteration
    updateConn = event::Events::ConnectWorldUpdateBegin(boost::bind(&Pose::Update, this, _1));
}

void Pose::Update(const common::UpdateInfo& info)
{
    float curr_time = model->GetWorld()->RealTime().Float();
    float delta_t = curr_time - lastTime;
    gzmsg << "Time : " << delta_t << " - Pose : " << model->WorldPose() << std::endl;
    lastTime = curr_time;
}
