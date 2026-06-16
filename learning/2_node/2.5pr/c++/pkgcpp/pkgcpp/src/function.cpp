#include "rclcpp/rclcpp.hpp"
class func :public rclcpp::Node
{
private:
    std::string p1_;
    int p2_;
public:
    func(const std::string &node_name, const std::string &p1, int p2):Node(node_name)
    {
        this->p1_ = p1;
        this->p2_ = p2;
    }
    void f2(const std::string &p3)
    {
        RCLCPP_INFO(this->get_logger(), "p1: %s, p2: %d, p3: %s", p1_.c_str(), p2_, p3.c_str());
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<func>("func_node", "param1", 123);
    RCLCPP_INFO(node->get_logger(), "infor");
    node->f2("param3");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
