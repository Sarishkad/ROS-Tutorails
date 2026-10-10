import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_path


def generate_launch_description():

    robot_description_path = os.path.join(
        get_package_share_path('my_robot_description'),
        'urdf',
        'my_arm.urdf.xacro'
    )

    rviz_config_path = os.path.join(
        get_package_share_path('my_robot_description'),
        'rviz',
        # 'arm_moveit_config.rviz'
        'arm_urdf_config.rviz'
    )

    controllers_config_path = os.path.join(
        get_package_share_path('my_robot_bringup'),
        'config',
        'ros2_controllers.yaml'
    )

    moveit_config_path = os.path.join(
        get_package_share_path('my_robot_moveit_config'),
        'launch',
        'move_group.launch.py'
    )

    robot_description = ParameterValue(
        Command(['xacro ', robot_description_path]),
        value_type=str
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'robot_description': robot_description}
        ],
        output='screen'
    )

    ros2_control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        name='controller_manager',
        parameters=[
            controllers_config_path,
            {'robot_description': robot_description}
        ],
        output='screen'
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager'
        ],
        output='screen'
    )

    arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'arm_controller',
            '--controller-manager',
            '/controller_manager'
        ],
        output='screen'
    )

    gripper_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'gripper_controller',
            '--controller-manager',
            '/controller_manager'
        ],
        output='screen'
    )

    move_group_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(moveit_config_path)
    )

    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        ros2_control_node,
        joint_state_broadcaster_spawner,
        arm_controller_spawner,
        gripper_controller_spawner,
        move_group_launch,
        rviz2_node
    ])
