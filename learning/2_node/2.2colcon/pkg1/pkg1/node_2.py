import rclpy
from rclpy.node import Node
def main():
    rclpy.init()
    node=Node("node2")
    node.get_logger().info("2")
    rclpy.spin(node)
    rclpy.shutdown()
 
