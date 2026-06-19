#include "rclcpp"
#include "geometry_msgs/msg/twist.hpp"
#include <chrono>
using namespace std::chrono_literals;//重载ms

class PublisherNode : public rclcpp::Node
{
private://指针
    rclcpp::TimerBase::SharedPtr t_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr p_;
public:
    explicit PublisherNode(const std::string & node_name) : Node(node_name)
    {
        p_ = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);  //核心
        t_ = this->create_wall_timer(100ms, std::bind(&PublisherNode::timer_callback, this));
    }
    void timer_callback()
    {
        auto msg = geometry_msgs::msg::Twist();
        msg.linear.x = 0.5;
        msg.angular.z = 0.2;
        p_->publish(msg);//发布
    };

}
int main(int argc, char* argv[])
{
     rclcpp::init(argc, argv);
    auto node = std::make_shared<PublisherNode>("pub_node");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}