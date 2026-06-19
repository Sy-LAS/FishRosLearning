import rclpy
from rclpy.node import Node
from interfaces.srv import FaceDetector
from ament_index_python.packages import get_package_share_directory
from cv_bridge import CvBridge
import cv2
from sensor_msgs.msg import Image
from rcl_interfaces.srv import SetParameters, Parameter, ParameterValue, ParameterType
from rcl_interfaces.msg import SetParametersResult

class FCS(Node):
    def __init__(self):
        super().__init__('f_d_s')
        self.client = self.create_client(FaceDetector, 'face_detect')
        self.bridge = CvBridge()
        self.test_image_path = get_package_share_directory(
            'face_srv')+'/resource/test.jpg'
        self.image = cv2.imread(self.test_image_path)
    def send_request(self):
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('服务未上线，等待中...')
        # 创建请求
        self.request = FaceDetector.Request()
        self.request.image = self.bridge.cv2_to_imgmsg(self.image, "bgr8")
        # 发送请求、等待(异步)
        future = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()
        self.get_logger().info('检测完成，耗时'+str(response.use_time))
        #self.show_face_locations(response),防止阻塞

    def call_set_param(self, param):
        client = self.create_client(SetParameters, 'set_parameters')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('等待参数....')
        request = SetParameters.Request()
        request.parameters = param
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        return response 
    
    def update_detect_model(self, model):
        # 创建参数
        param= Parameter()
        param.name = "model"
        # 创建参数值
        new_model_value = ParameterValue()
        new_model_value.type = ParameterType.PARAMETER_STRING
        new_model_value.string_value = model
        param.value = new_model_value
        # 请求更新并处理
        response = self.call_set_param([param])
        for result in response.results:
            if result.successful:
                self.get_logger().info(f'参数 {param.name} 设置为{model}')
            else:
                self.get_logger().info(f'参数设置失败，原因为：{result.reason}')
    def show_face_locations(self, response):
        self.get_logger().info('检测到'+str(response.num)+'张人脸')
        for i in range(response.num):
            top=response.top[i]
            right=response.right[i]
            bottom=response.bottom[i]
            left=response.left[i]
            cv2.rectangle(self.image, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.imshow('image', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
def main(args=None):
    rclpy.init(args=args)
    f_c_n = FCS()
    f_c_n.update_detect_model('hog')
    f_c_n.send_request()
    f_c_n.update_detect_model('cnn')
    rclpy.spin(f_c_n)
    f_c_n.destroy_node()
    rclpy.shutdown()
