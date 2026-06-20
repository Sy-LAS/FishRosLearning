import launch
import launch_ros
from ament_index_python.packages import get_package_share_directory
def generate_launch_description():
    a_d_start_rqt_ = launch.actions.DeclareLaunchArgument('start_rqt', default_value='False')
    #替换
    start_rqt = launch.substitutions.LaunchConfiguration('start_rqt')
    #动作1-嵌套
    launch_path_ = [get_package_share_directory('tur_control'), '/launch', '/tur.launch.py']
    action_nested = launch.actions.IncludeLaunchDescription(
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            launch_path_
        )
    )
    #动作2-打印
    action_print = launch.actions.LogInfo(
        msg=[str(launch_path_)]
    )
    #动作3-执行
    action_execute = launch.actions.ExecuteProcess(
        cmd=['rqt'],
    #条件判断
        condition=launch.conditions.IfCondition(start_rqt)
    )
    #动作4-组织
    action_group = launch.actions.GroupAction([
    #动作5-定时
        launch.actions.TimerAction(period=2.0,actions=[action_nested]),
        launch.actions.TimerAction(period=5.0,actions=[action_execute]),
    ])
    return launch.LaunchDescription([
        a_d_start_rqt_,
        action_print,
        action_group
    ])
