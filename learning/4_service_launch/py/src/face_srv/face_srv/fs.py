import face_recognition
import cv2
from ament_index_python.packages import get_package_share_directory#获取功能吧share目录绝对路径

def main():
    # 获取图片真实路径
    defaut_image_path = get_package_share_directory(
        'face_srv')+'/resource/default.jpg'
    print(f"图片绝对路径："+ {defaut_image_path})
    # 使用 opencv 加载图像
    image = cv2.imread(defaut_image_path)
    # 查找图像中所有的人脸
    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=1, model='hog')
    print("I found {} face(s) in this photograph.".format(len(face_locations)))
    # 创建边框
    for top, right, bottom, left in face_locations:
        cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 4)
    # 结果显示
    cv2.imshow('Face Detection', image)
    cv2.waitKey(0)
