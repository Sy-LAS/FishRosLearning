import rclpy
from rclpy.node import Node

def main():
    rclpy.init()
    node=Node("first_python")
    node.get_logger().info("1")
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()
