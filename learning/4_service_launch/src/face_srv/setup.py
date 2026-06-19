from setuptools import find_packages, setup

package_name = 'face_srv'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + "/resource", [ 'resource/top.png']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='chuil',
    maintainer_email='Yingkai.Shao25@student.xjtlu.edu.cn',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'fs = face_srv.fs:main',
            'f_d_n = face_srv.f_d_n:main',
            'f_c_n = face_srv.f_c_n:main',
        ],
    },
)
