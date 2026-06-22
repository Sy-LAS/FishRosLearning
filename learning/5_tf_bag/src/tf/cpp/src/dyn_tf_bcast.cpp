#include <memory>
#include "geometry_msgs/msg/transform_stamped.hpp" // 提供消息接口
#include "rclcpp/rclcpp.hpp"
#include "tf2/LinearMath/Quaternion.h"             // 提供 tf2::Quaternion 类
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp" // 提供消息类型转换函数
#include "tf2_ros/transform_broadcaster.h"         // 提供坐标广播器类
#include <chrono>                                  // 引入时间相关头文件
// 使用时间单位的字面量，可以在代码中使用 s 和 ms 表示时间
using namespace std::chrono_literals;

class DynTFBcast : public rclcpp::Node {
 public:
  DynTFBcast() : Node("dynamic_tf_broadcaster") {
    tf_bcast_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);
    t_ = create_wall_timer(10ms, std::bind(&DynTFBcast::pubTf, this));
  }

  void pubTf() {
    geometry_msgs::msg::TransformStamped tf;
    tf.header.stamp = this->get_clock()->now();
    tf.header.frame_id = "map";
    tf.child_frame_id = "base_link";
    tf.transform.translation.x = 2.0;
    tf.transform.translation.y = 3.0;
    tf.transform.translation.z = 0.0;
    tf2::Quaternion quat;
    quat.setRPY(0, 0, 30 * M_PI / 180);         // 弧度制欧拉角转四元数
    tf.transform.rotation = tf2::toMsg(quat);    // 转成消息接口类型
    tf_bcast_->sendTransform(tf);
  }

 private:
  std::shared_ptr<tf2_ros::TransformBroadcaster> tf_bcast_;
  rclcpp::TimerBase::SharedPtr t_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<DynTFBcast>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
