import rclpy
from rclpy.node import Node
from tf2_ros import TransformListener, Buffer#改
from tf_transformations import euler_from_quaternion
import math
class TFB(Node):
    def __init__(self):
        super().__init__('tf_broadcaster')
        self.buf_=Buffer()
        self.lis_=TransformListener(self.buf_,self)
        self.t_=self.create_timer(1.0,self.get_tf_)
    def get_tf_(self):
        try:
            r_=self.buf_.lookup_transform('base_link','camera_link',rclpy.time.Time(0),rclpy.time.Duration(1.0))
            tf_=r_.transform
            self.get_logger().info(f'平移:{tf_}')
            self.get_logger().info(f'旋转:{tf_.rotation}')
            rot_eul=euler_from_quaternion([tf_.rotation.x,tf_.rotation.y,tf_.rotation.z,tf_.rotation.w])
            self.get_logger().info(f'旋转RPY:{rot_eul}')
            self.get_logger().info(f'平移:{tf_.translation.y}')

        except Exception as e:
            pass
            self.get_logger().info(f'未找到tf:{e}')
def main():
    rclpy.init()
    node=TFB()
    rclpy.spin(node)
    rclpy.shutdown()

