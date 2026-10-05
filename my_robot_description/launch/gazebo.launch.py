import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_path


def generate_launch_description():

    urdf_path = os.path.join(
        get_package_share_path('my_robot_description'),
        'urdf',
        'my_robot.urdf.xacro'
    )

    gazebo_config_path = os.path.join(
        get_package_share_path('my_robot_description'),
        'config',
        'gazebo_bridge.yaml'
    )

    rviz_config_path = os.path.join(
        get_package_share_path('my_robot_description'),
        'rviz',
        'urdf_config.rviz'
    )

    world_path = os.path.join(
        get_package_share_path('my_robot_description'),
        'worlds',
        'test_world.sdf'
    )

    robot_description = ParameterValue(
        Command(['xacro ', urdf_path]),
        value_type=str
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                'robot_description': robot_description
            }
        ],
        output='screen'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_path('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            # 'gz_args': f'{world_path} -r'
            'gz_args': '-r empty.sdf'
        }.items()
    )

    gazebo_spawn_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic',
            'robot_description'
        ],
        output='screen'
    )

    ros_gz_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[
            {
                'config_file': gazebo_config_path
            }
        ],
        output='screen'
    )

    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=[
            '-d',
            rviz_config_path
        ],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        gazebo,
        gazebo_spawn_node,
        ros_gz_bridge_node,
        rviz2_node
    ])