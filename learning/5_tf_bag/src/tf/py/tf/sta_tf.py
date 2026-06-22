import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
from tf_transformations import quaternion_from_euler
import math

class STFBroadcaster(Node):
    def __init__(self):
        super().__init__('stf_broadcaster')
        self.stfb_=TransformBroadcaster(self)
        self.publish_tf_()

    def publish_tf_(self):
        t_=TransformStamped()
        t_.header.stamp=self.get_clock().now().to_msg()
        t_.header.frame_id='base_link'
        t_.child_frame_id='camera_link'
        t_.transform.translation.x=0.5
        t_.transform.translation.y=0.0
        t_.transform.translation.z=0.0
        q_=quaternion_from_euler(math.radians(180),0,0)
        t_.transform.rotation.x=q_[0]
        t_.transform.rotation.y=q_[1]
        t_.transform.rotation.z=q_[2]
        t_.transform.rotation.w=q_[3]
        self.stfb_.sendTransform(t_)
        self.get_logger().info(f'发布静态tf:{t_}')
def main():
    rclpy.init()
    node=STFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()
