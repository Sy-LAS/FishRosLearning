import espeakng
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue
import threading
import time

class SubscriberNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name}启动')
        self.q = Queue()

        self.s_ = self.create_subscription(String, 'topic',self.sub_callback, 10)#核心

        self.t_ = threading.Thread(target=self.speak_thread)
        self.t_.start()

        def sub_callback(self, msg):
            self.q.put(msg.data)
        def speak_thread(self):
            speaker = espeakng.Speaker()
            speaker.set_voice('zh-CN')
            while rclpy.ok():
                if not self.q.empty():
                    t_=self.q.get()
                    self.get_logger().info(f'开始: {t_}')
                    speaker.say(t_)
                    speaker.wait()
                else:#降CPU
                    time.sleep(1)

def main(self):
    rclpy.init()
    node = SubscriberNode('sub_node')
    rclpy.spin(node)
    rclpy.shutdown()