#include <chrono>
#include <cstdlib>
#include <ctime>
#include <rclcpp/rclcpp.hpp>
#include "interfaces/srv/patrol.hpp"
#include "rcl_interfaces/msg/parameter.hpp"
#include "rcl_interfaces/srv/set_parameters.hpp"
#include "rcl_interfaces/msg/parameter_type.hpp"
#include "rcl_interfaces/msg/parameter_value.hpp"
using namespace std::chrono_literals;
using Patrol = interfaces::srv::Patrol;
using SetP = rcl_interfaces::srv::SetParameters;

class PatrolClient : public rclcpp::Node
{
public:
  PatrolClient(): Node("patrol_client")
  {
    pat_cli_=this->create_client<Patrol>("patrol");
    timer=this->create_wall_timer(10s, std::bind(&PatrolClient::timer_callback, this));
    srand(time(0));//随机化初始种子（以当前时间点）
  }
  void update_param_k(double k)
  { //创建参数
    auto p_ = rcl_interfaces::msg::Parameter();
    p_.name = "k";
    //参数值
    auto pv = rcl_interfaces::msg::ParameterValue();
    pv.type = rcl_interfaces::msg::ParameterType::PARAMETER_DOUBLE;
    pv.double_value = k;
    p_.value=pv;
    //更新
    auto r_ =set_param(p_);
    if (r_.get() == nullptr)
    {
        RCLCPP_ERROR(this->get_logger(), "改参k失败");
        return;
    }
    else
    {
        for (const auto & res : r_->results)
        {
            if (res.successful)
            {
                RCLCPP_INFO(this->get_logger(), "改参k成功");
                return;
            }
            else
            {
                RCLCPP_ERROR(this->get_logger(), "改参失败");
                return;
            }
        }
    }
  }
  std::shared_ptr<SetP::Response> set_param(rcl_interfaces::msg::Parameter &p_)
  {  //创建客户端
    auto par_cli = this->create_client<SetP>("/tur_control/set_parameters");
    while (!par_cli->wait_for_service(std::chrono::seconds(1)))
    {
        if (!rclcpp::ok())
        {
            RCLCPP_ERROR(this->get_logger(), "等待服务端超时");
            return nullptr;
        }
        RCLCPP_INFO(this->get_logger(), "等待服务端...");
    }
    //创建请求，异步调用
    auto request = std::make_shared<SetP::Request>();
    request->parameters.push_back(p_);
    auto future = par_cli->async_send_request(request);
    rclcpp::spin_until_future_complete(this->get_node_base_interface(), future);
    auto response = future.get();
    return response;
    }

    void timer_callback()
    {
        //等服务端上线
        while (!pat_cli_->wait_for_service(std::chrono::seconds(1)))
        {
            if (!rclcpp::ok())
            {
                RCLCPP_ERROR(this->get_logger(), "等待服务端时被打断");
                return;
            }
            RCLCPP_INFO(this->get_logger(), "等待服务端...");
        }
        //构造请求
        auto r_ = std::make_shared<Patrol::Request>();
        r_->target_x=rand()%15;
        r_->target_y=rand()%15;
        RCLCPP_INFO(this->get_logger(), "发送巡逻: (%f,%f)", r_->target_x, r_->target_y);
        pat_cli_->async_send_request(r_, [&](rclcpp::Client<Patrol>::SharedFuture future)
        ->void
        {
            auto r_ = future.get();
            if (r_->result == Patrol::Response::SUCCESS)
            {
                RCLCPP_INFO(this->get_logger(), "目标点处理成功");
            }
            else if (r_->result==Patrol::Response::FAIL)
            {
                RCLCPP_INFO(this->get_logger(), "目标点处理失败");
            }
        });
    }
private:
  rclcpp::Client<Patrol>::SharedPtr pat_cli_;
  rclcpp::TimerBase::SharedPtr timer;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<PatrolClient>();
  node->update_param_k(1.0);
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
