import rclpy
from status_interfaces.msg import SystemStatus
from rclpy.node import Node
import psutil
import platform

class pub(Node):
    def __init__(self):
        super().__init__('pub')
        self.p_ = self.create_publisher(SystemStatus, 'system_status', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
    def timer_callback(self):
        msg = SystemStatus()
        msg.stamp = self.get_clock().now().to_msg()
        msg.hostname = platform.node()
        msg.cpu_percent = psutil.cpu_percent()
        msg.memory_percent = psutil.virtual_memory().percent
        msg.memory_total = psutil.virtual_memory().total/1024/1024
        msg.memory_available = psutil.virtual_memory().available/1024/1024
        msg.net_sent = psutil.net_io_counters().bytes_sent/1024/1024
        msg.net_recv = psutil.net_io_counters().bytes_recv/1024/1024
        self.get_logger().info('Publishing: "%s"' % msg)
        self.p_.publish(msg)
def main():
    rclpy.init()
    node=pub()
    rclpy.spin(node)
    node.destroy_node()
