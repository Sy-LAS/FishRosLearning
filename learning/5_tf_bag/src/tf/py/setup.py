from setuptools import find_packages, setup

package_name = 'tf'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
            'stf=tf.sta_tf:main',
            'dta_tf=tf.dta_tf:main',
            'tf_lis=tf.tf_lis:main',
        ],
    },
)
