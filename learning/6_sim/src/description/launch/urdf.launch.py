import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_path = get_package_share_directory('description')
    urdf_path = os.path.join(pkg_path, 'urdf', 'rob.urdf')
    declare_argmodel_path = launch.actions.DeclareLaunchArgument(name='model',
        default_value=str(urdf_path), description='URDF path')
    commend_ = launch.substitutions.Command(
        ['cat ', launch.substitutions.LaunchConfiguration('model')])
    des_value_=launch_ros.parameter_descriptions.ParameterValue(
        commend_, value_type=str)

    rob_pub=launch_ros.actions.Node(
        package='robot_state_publisher', 
        executable='robot_state_publisher', 
        parameters=[{'robot_description': des_value_}],
        output='screen')
    joint_pub=launch_ros.actions.Node(
        package='joint_state_publisher', 
        executable='joint_state_publisher', 
        output='screen')
    rviz_pub=launch_ros.actions.Node(
        package='rviz2', 
        executable='rviz2', 
        output='screen')
    return launch.LaunchDescription([
        declare_argmodel_path, rob_pub, joint_pub, rviz_pub
    ])
