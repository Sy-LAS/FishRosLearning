#include "rclcpp/rclcpp.hpp"
int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<rclcpp::Node>("node_1");
    RCLCPP_INFO(node->get_logger(),"2");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

//第 2 行：char** argc 应为 char** argv
//第 6 行：rclcp 拼写错误，应为 rclcpp
//第 7 行：rclcpp::shutdown 缺少括号 ()
//第 8 行：return 0 缺少分号 ;
