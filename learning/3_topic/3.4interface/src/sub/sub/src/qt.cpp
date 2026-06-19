#include <QApplication>
#include <QLabel>
#include <QString>
#include <rclcpp/rclcpp.hpp>
#include <status_interfaces/msg/system_status.hpp>
#include <thread>
#include <sstream>


using SS = status_interfaces::msg::SystemStatus;

class sub : public rclcpp::Node
{
private:
    rclcpp::Subscription<SS>::SharedPtr sub_;
    QLabel* l_;
public:
    sub(): Node("SysStatus_sub")
    {
        l_ = new QLabel();
        sub_ = this->create_subscription<SS>(
            "system_status", 10,
            [&](const SS::SharedPtr msg)->void {
                l_->setText(get_qstring_from_msg(msg));
            });
        l_->setText(get_qstring_from_msg(std::make_shared<SS>()));
        l_->show();
    }
    QString get_qstring_from_msg(const SS::SharedPtr msg)
    {
        std::stringstream show_str;
        show_str << "============系统状态==============\n"
            << "数据时间: " << msg->stamp.sec << "\ts\n"
            << "主机名: " << msg->hostname << "\t\n"
            << "CPU使用率: " << msg->cpu_percent << "\t%\n"
            << "内存使用率: " << msg->memory_percent << "\t%\n"
            << "内存总大小: " << msg->memory_total << "\tMB\n"
            << "内存可用大小: " << msg->memory_available  << "\tMB\n"
            << "网络发送: " << msg->net_sent << "\tMB\n"
            << "网络接收: " << msg->net_recv << "\tMB\n"
            << "=====================================";
        return QString::fromStdString(show_str.str());
    }
};


int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    QApplication app(argc, argv);
    auto node = std::make_shared<sub>();
    std::thread([&]()->void {
        rclcpp::spin(node);
    }).detach();
    app.exec();
    return 0;
}


