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
       # 因版本问题，有别于fishros
    spawn_entity=launch_ros.actions.Node(
        package='ros_gz_sim', 
        executable='create', 
        arguments=['-topic', '/robot_description',
                   '-name', 'bot'])
    # 桥接 Ignition Transport <-> ROS 2(非fishros内容)
    bridge=launch_ros.actions.Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[ignition.msgs.Odometry',
            '/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
        ],
        output='screen')

    load_joint_state_controller=launch_ros.actions.Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_controller', '--controller-manager', '/controller_manager']
    )

    load_bot_effort_controller=launch_ros.actions.Node(
        package='controller_manager',
        executable='spawner',
        arguments=['fishbot_effort_controller', '--controller-manager', '/controller_manager']
    )

    load_bot_diff_drive_controller=launch_ros.actions.Node(
        package='controller_manager',
        executable='spawner',
        arguments=['fishbot_diff_drive_controller', '--controller-manager', '/controller_manager']
    )
    return launch.LaunchDescription([
        declare_argmodel_path, rob_pub, gz, spawn_entity, bridge,
        # 事件动作，定义先后
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=spawn_entity,
                on_exit=[load_joint_state_controller],)
        ),
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=load_joint_state_controller,
                on_exit=[load_bot_diff_drive_controller],)
        ),
    ])

