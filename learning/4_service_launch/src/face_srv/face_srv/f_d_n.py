import rclpy
from rclpy.node import Node
from interfaces.srv import FaceDetector
from ament_index_python.packages import get_package_share_directory
from cv_bridge import CvBridge
import cv2
import face_recognition
import time
from rcl_interfaces.msg import SetParametersResult

class FDS(Node):
    def __init__(self):
        super().__init__('f_d_s')
        self.bridge = CvBridge()
        self.srv = self.create_service(FaceDetector, 'fd', self.fd_callback)
        self.default_image_path = get_package_share_directory('face_srv')+'/resource/default.jpg'
        self.upsample_times = 1
        self.model = "hog"
        # 声明获取参数
        self.declare_parameter('face_locations_upsample_times', 1)
        self.declare_parameter('face_locations_model', "hog")
        self.upsample_times = self.get_parameter("face_locations_upsample_times").value
        self.model = self.get_parameter("face_locations_model").value
        self.set_parameters([rclpy.Parameter('face_locations_upsample_times', rclpy.Parameter.Type.INT, self.upsample_times),
                            rclpy.Parameter('face_locations_model', rclpy.Parameter.Type.STRING, self.model)])
        self.add_on_set_parameters_callback(self.parameter_callback)
    def parameter_callback(self, parameters):
        for parameter in parameters:
            self.get_logger().info(
                f'参数 {parameter.name} 设置为：{parameter.value}')
            if parameter.name == 'face_locations_upsample_times':
                self.upsample_times = parameter.value
            elif parameter.name == 'face_locations_model':
                self.model = parameter.value
            return SetParametersResult(successful=True)
    def fd_callback(self, request, response):
        self.get_logger().info('接收到请求')
        if request.image.data:
            cv_image = self.bridge.imgmsg_to_cv2(request.image, "bgr8")
        else:
            cv_image = cv2.imread(self.default_image_path)
        start_time = time.time()
        self.get_logger().info('图像已加载，开始检测')
        face_locations = face_recognition.face_locations(cv_image, self.upsample_times, self.model)
        end_time = time.time()
        self.get_logger().info('检测完成，耗时'+str(end_time-start_time))
        response.num = len(face_locations)
        response.use_time = end_time - start_time
        for top,right,bottom,left in face_locations:
            response.right.append(right)
            response.top.append(top)
            response.left.append(left)
            response.bottom.append(bottom)
        return response
def main(args=None):
    rclpy.init(args=args)
    node = FDS()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
