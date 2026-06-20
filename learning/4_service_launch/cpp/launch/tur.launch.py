import launch
import launch_ros
def generate_launch_description():

    action_declare_arg_bg_g = launch.actions.DeclareLaunchArgument('background_g', default_value='0.0')
    turcrl_=launch_ros.actions.Node(
        package='tur_control',
        executable='turtle',
        parameters=[{'background_g': launch.substitutions.LaunchConfiguration('background_g')}],
        name='tur_control'
    )
    trusim_=launch_ros.actions.Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim_node'
    )

    return launch.LaunchDescription([
        action_declare_arg_bg_g,
        turcrl_,
        trusim_
    ])
