from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()
    
    robot_news_station = Node(
        package="my_py_pkg",
        executable="robot_news_station",
        remappings=[("/robot_news", "/my_news")],
        parameters=[
            {"timer_period": 1.0},
        ]
    )
    
    smartphone = Node(
        package="my_cpp_pkg",
        executable="smartphone",
        remappings=[("/robot_news", "/my_news")],
    )
    
    ld.add_action(robot_news_station)
    ld.add_action(smartphone)
    
    return ld