import rclpy
from rclpy.node import Node

class pyl(Node):
    def __init__(self, node_name: str, p_1_value: str, p_2_value: str) -> None:
        super().__init__(node_name)
        self.p_1 = p_1_value
        self.p_2 = p_2_value
    
    def func(self,p_3:str):
        print(f"p_1: {self.p_1}, p_2: {self.p_2}, p_3: {p_3}")
        self.get_logger().info(f"p_1: {self.p_1}, p_2: {self.p_2}, p_3: {p_3}")
def main():
    rclpy.init()
    node=pyl("py1","value_1", "value_2")
    node.func("value_3")
    rclpy.spin(node)
    rclpy.shutdown()
