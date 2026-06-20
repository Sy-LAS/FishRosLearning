import launch
import launch_ros
def generate_launch_description():
    turcrl_=launch_ros.actions.Node(
        package='tur_control',
        executable='turtle',
        name='tur_control'
    )
    trusim_=launch_ros.actions.Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim_node'
    )

    return launch.LaunchDescription([
        turcrl_,
        trusim_
    ])
