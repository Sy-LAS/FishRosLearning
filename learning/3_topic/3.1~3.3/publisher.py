import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
from queue import Queue

class TopicNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name}启动')

        self.q = Queue()#放在较前面,防止回调函数出错

        self.p_ = self.create_publisher(String, 'topic', 10) #核心
        timer_period = 0.5  # 定义间隔时间
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):#回调函数
        if self.q.qsize() > 0: 
            m_ = self.q.get() #从队列中取出数据
            ms = String()
            ms.data = m_
            self.p_.publish(ms) #发布数据
            self.get_logger().info(f'发布数据: {ms.data}')
    def func(self):
        #函数功能
        pass


def main(self):
    rclpy.init()
    n = TopicNode('pub_node')
    rclpy.spin(n)
    #n.destroy_node()
    rclpy.shutdown()