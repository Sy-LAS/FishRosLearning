#include <memory>
#include "geometry_msgs/msg/transform_stamped.hpp"  // 提供消息接口
#include "rclcpp/rclcpp.hpp"
#include "tf2/LinearMath/Quaternion.h"  // 提供 tf2::Quaternion 类
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"  // 提供消息类型转换函数
#include "tf2_ros/static_transform_broadcaster.h"  // 提供静态坐标广播器类

class StaticTFBcast : public rclcpp::Node {
 public:
  StaticTFBcast() : Node("tf_broadcaster_node") {
    // 创建静态广播发发布器并发布
    bcast_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);
    this->pub_tf();
  }

  void pub_tf() {
    geometry_msgs::msg::TransformStamped tf;
    tf.header.stamp = this->get_clock()->now();
    tf.header.frame_id = "map";
    tf.child_frame_id = "target_point";
    tf.transform.translation.x = 5.0;
    tf.transform.translation.y = 3.0;
    tf.transform.translation.z = 0.0;
    tf2::Quaternion quat;
    quat.setRPY(0, 0, 60 * M_PI / 180);  // 弧度制欧拉角转四元数
    tf.transform.rotation = tf2::toMsg(quat);  // 转成消息接口类型
    bcast_->sendTransform(tf);
  }

 private:
  std::shared_ptr<tf2_ros::StaticTransformBroadcaster> bcast_;
};

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<StaticTFBcast>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
