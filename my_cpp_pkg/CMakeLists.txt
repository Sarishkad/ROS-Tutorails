cmake_minimum_required(VERSION 3.8)
project(my_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(example_interfaces REQUIRED)
find_package(my_robot_interfaces REQUIRED)
find_package(rclcpp_action REQUIRED)

add_executable(test_node src/test_node.cpp)
ament_target_dependencies(test_node
  rclcpp
)

add_executable(robot_news_station src/robot_news_station.cpp)
ament_target_dependencies(robot_news_station
  rclcpp
  example_interfaces
)

add_executable(add_two_ints_server src/add_two_ints_server.cpp)
ament_target_dependencies(add_two_ints_server
  rclcpp
  example_interfaces
)

add_executable(add_two_ints_client src/add_two_ints_client.cpp)
ament_target_dependencies(add_two_ints_client
  rclcpp
  example_interfaces
)

add_executable(smartphone src/smartphone.cpp)
ament_target_dependencies(smartphone
  rclcpp
  example_interfaces
)

add_executable(hardware_status_pub src/hardware_status_pub.cpp)
ament_target_dependencies(hardware_status_pub
  rclcpp 
  my_robot_interfaces 
)

add_executable(count_until_server src/count_until_action_server.cpp)
ament_target_dependencies(count_until_server
  rclcpp 
  my_robot_interfaces
  rclcpp_action 
)


add_executable(count_until_action_server_queue_goals src/count_until_action_server_queue_goals.cpp)
ament_target_dependencies(count_until_action_server_queue_goals
  rclcpp 
  my_robot_interfaces
  rclcpp_action 
)

add_executable(count_until_client src/count_until_action_client.cpp)
ament_target_dependencies(count_until_client
  rclcpp 
  my_robot_interfaces
  rclcpp_action 
)

install(TARGETS
  test_node
  robot_news_station
  smartphone
  hardware_status_pub
  add_two_ints_server
  add_two_ints_client
  count_until_server
  count_until_action_server_queue_goals
  count_until_client
  
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
