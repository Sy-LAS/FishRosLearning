import rclpy
from pkg1.pyl import pyl


class ppyl(pyl):
    def __init__ (self, p_1_value: str, p_2_value: str, p_s_value: str) -> None:
        super().__init__("ppyl_node", p_1_value, p_2_value)
        self.p_s = p_s_value


def main():
    rclpy.init()
    node = ppyl("value_1", "value_2", "value_s")
    node.func("value_3")
    rclpy.spin(node)
    rclpy.shutdown()
