import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_path = get_package_share_directory('description')
    default_xacro_path = os.path.join(pkg_path, 'urdf', 'bot', 'bot.urdf.xacro')
    default_gz_path = os.path.join(pkg_path, 'world', 'default.sdf')
    declare_argmodel_path = launch.actions.DeclareLaunchArgument(name='model',
        default_value=str(default_xacro_path), description='URDF path')
    commend_ = launch.substitutions.Command(
        ['xacro ', launch.substitutions.LaunchConfiguration('model')])
    des_value_=launch_ros.parameter_descriptions.ParameterValue(
        commend_, value_type=str)

    rob_pub=launch_ros.actions.Node(
        package='robot_state_publisher', 
        executable='robot_state_publisher', 
        parameters=[{'robot_description': des_value_}],
        output='screen')
    gz=launch.actions.ExecuteProcess(
        cmd=['ign', 'gazebo', '-s', default_gz_path], output='screen')
    spawn_entity=launch_ros.actions.Node(
        package='ros_gz_sim', 
        executable='create', 
        arguments=['-topic', '/robot_description',
                   '-name', 'bot'])
    # 桥接 Ignition Transport <-> ROS 2
    bridge=launch_ros.actions.Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
        ],
        output='screen')

    return launch.LaunchDescription([
        declare_argmodel_path, rob_pub, gz, spawn_entity, bridge
    ])
