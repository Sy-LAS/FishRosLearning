#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "turtlesim/msg/pose.hpp"
#include "interfaces/srv/patrol.hpp"
#include "rcl_interfaces/msg/set_parameters_result.hpp"
using Patrol=interfaces::srv::Patrol;
using SetParamResult=rcl_interfaces::msg::SetParametersResult;

class TurControl:public rclcpp::Node
{ 
private:
    rclcpp::Service<Patrol>::SharedPtr pat_ser_;
    rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr pos_sub_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr vel_pub_;
    double tar_x_{1.0};
    double tar_y_{1.0};
    double k_{1.0};
    double max_spe_{1.0};
    OnSetParametersCallbackHandle::SharedPtr par_cb_han_;

    void pos_rec_(const turtlesim::msg::Pose::SharedPtr pose)
    {
    auto message = geometry_msgs::msg::Twist();
    double current_x = pose->x;
    double current_y = pose->y;
    RCLCPP_INFO(this->get_logger(), "当前位置:(x=%f,y=%f)", current_x, current_y);
    double distance =
        std::sqrt((tar_x_ - current_x) * (tar_x_ - current_x) +
                  (tar_y_ - current_y) * (tar_y_ - current_y));
    double angle =
        std::atan2(tar_y_ - current_y, tar_x_ - current_x) - pose->theta;
    if (distance > 0.1) {
      if(fabs(angle)>0.2)
      {
        message.angular.z = fabs(angle);
      }else{
        message.linear.x = k_ * distance;
      }
    }
    if (message.linear.x > max_spe_) {
       message.linear.x = max_spe_;
    }
    vel_pub_->publish(message);
    }

public:
    TurControl():Node("tur_control")
    {
        vel_pub_=this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel",10);
        pos_sub_=this->create_subscription<turtlesim::msg::Pose>("turtle1/pose",10,std::bind(&TurControl::pos_rec_,this,std::placeholders::_1));
        pat_ser_=this->create_service<Patrol>
        (
            "patrol",[&](const std::shared_ptr<Patrol::Request> request,std::shared_ptr<Patrol::Response> response)->void
            {
            if((0<request->target_x && request->target_x<12.0f) && (0<request->target_y && request->target_y<12.0f))
            {
                tar_x_=request->target_x;
                tar_y_=request->target_y;
                response->result=Patrol::Response::SUCCESS;
            }else{
                response->result=Patrol::Response::FAIL;
                 }
            }
        );
        this->declare_parameter("k",1.0);
        this->get_parameter("k",k_);
        this->declare_parameter("max_speed",1.0);
        this->get_parameter("max_speed",max_spe_);

    par_cb_han_ = this->add_on_set_parameters_callback(
        [&](const std::vector<rclcpp::Parameter>& parameters)-> SetParamResult {
            for (auto param : parameters) {
            RCLCPP_INFO(this->get_logger(), "更新参数 %s 值为：%f", param.get_name().c_str(), param.as_double());
            if (param.get_name() == "k"){
                k_=param.as_double();    }
                else if (param.get_name() == "max_speed")
                {
                    max_spe_=param.as_double();
                }
            }
            auto result = SetParamResult();
            result.successful = true;
            return result;
        });
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<TurControl>());
    rclcpp::shutdown();
    return 0;
}