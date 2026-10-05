# ROS 2 Tutorials & Robot Simulation Workspace

Welcome to the **ROS 2 Tutorials & Simulation** repository. This workspace contains a comprehensive set of hands-on packages demonstrating fundamental to advanced robotics development concepts in **ROS 2 (Jazzy / Humble)** using both **C++ (`rclcpp`)** and **Python (`rclpy`)**, alongside custom interfaces, executors, component composition, launch files, and URDF/Gazebo robot simulation.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Workspace Architecture](#-workspace-architecture)
- [Prerequisites](#-prerequisites)
- [Build and Installation](#-build-and-installation)
- [Packages and Modules](#-packages-and-modules)
  - [1. my_robot_interfaces](#1-my_robot_interfaces)
  - [2. my_py_pkg (Python Nodes)](#2-my_py_pkg-python-nodes)
  - [3. my_cpp_pkg (C++ Nodes)](#3-my_cpp_pkg-c-nodes)
  - [4. my_robot_description (URDF & Simulation)](#4-my_robot_description-urdf--simulation)
  - [5. my_robot_bringup (Launch System)](#5-my_robot_bringup-launch-system)
  - [6. executors_py & executors_cpp](#6-executors_py--executors_cpp)
  - [7. components_py & components_cpp](#7-components_py--components_cpp)
  - [8. my_mix_pkg](#8-my_mix_pkg)
- [Tutorial Walkthrough & Running Examples](#-tutorial-walkthrough--running-examples)
  - [Publishers and Subscribers](#publishers-and-subscribers)
  - [Services (Client / Server)](#services-client--server)
  - [Custom Messages](#custom-messages)
  - [Actions (Feedback & Goal Queuing)](#actions-feedback--goal-queuing)
  - [Launch Files and Remapping](#launch-files-and-remapping)
  - [Executors & Concurrency](#executors--concurrency)
  - [Component Composition](#component-composition)
  - [Robot Model in RViz2](#robot-model-in-rviz2)
  - [Robot Simulation in Gazebo Sim](#robot-simulation-in-gazebo-sim)
- [Gazebo Bridge Topics](#-gazebo-bridge-topics)
- [Troubleshooting & Tips](#-troubleshooting--tips)
- [License](#-license)

---

## 🚀 Overview

This repository is designed as a structured guide and testing ground for modern ROS 2 programming patterns:

- **Core Communication Patterns:** Topics (pub/sub), Services (client/server), and Actions (goal, feedback, result, cancel, queuing).
- **Dual-Language Parity:** Core nodes implemented in both modern **C++ (C++17 / `rclcpp`)** and **Python 3 (`rclpy`)**.
- **Custom Interfaces:** Defining custom `.msg`, `.srv`, and `.action` files in dedicated interface packages.
- **Advanced Concurrency:** Comparing Single-Threaded and Multi-Threaded Executors, understanding re-entrant and mutually exclusive callback groups.
- **Composition & Components:** Writing modular ROS 2 components loaded into container processes vs. manual composition.
- **Robot Modeling:** Parameterized **Xacro / URDF** mobile base (differential drive + caster wheel + camera sensor).
- **Simulation:** Integration with **Gazebo Sim (`ros_gz`)**, differential drive plugin, sensor simulation, and `ros_gz_bridge`.

---

## 📂 Workspace Architecture

```plaintext
src/
├── my_robot_interfaces/     # Custom ROS 2 msg, srv, and action definitions
├── my_py_pkg/              # Python nodes (Pub/Sub, Service, Action, Custom msg)
├── my_cpp_pkg/             # C++ nodes (Pub/Sub, Service, Action, Goal Queuing)
├── my_robot_bringup/       # Launch files and parameter configurations
├── my_robot_description/   # Robot Xacro/URDF, RViz configs, Gazebo worlds & bridge
├── executors_py/           # Python single vs. multi-threaded executor demos
├── executors_cpp/          # C++ single vs. multi-threaded executor demos
├── components_py/          # Python manual node composition
├── components_cpp/         # C++ rclcpp_components & manual composition
├── my_mix_pkg/             # Template for mixed C++ and Python package
└── README.md               # Repository documentation
```

---

## 🛠 Prerequisites

- **ROS 2 Distribution:** ROS 2 Jazzy Jalisco (Ubuntu 24.04) or ROS 2 Humble Hawksbill (Ubuntu 22.04).
- **Gazebo Sim:** Gazebo Harmonic (Jazzy) or Gazebo Fortress (Humble).
- **Required ROS 2 Packages:**
  ```bash
  sudo apt update
  sudo apt install -y \
    python3-colcon-common-extensions \
    ros-$ROS_DISTRO-xacro \
    ros-$ROS_DISTRO-joint-state-publisher-gui \
    ros-$ROS_DISTRO-robot-state-publisher \
    ros-$ROS_DISTRO-rviz2 \
    ros-$ROS_DISTRO-ros-gz \
    ros-$ROS_DISTRO-teleop-twist-keyboard
  ```

---

## 🔨 Build and Installation

From the root of the workspace (`~/ros_ws`):

```bash
# 1. Source ROS 2 base environment
source /opt/ros/$ROS_DISTRO/setup.bash

# 2. Resolve dependencies (optional but recommended)
rosdep update
rosdep install --from-paths src --ignore-src -r -y

# 3. Build workspace
colcon build --symlink-install

# 4. Source the local workspace overlay
source install/setup.bash
```

> **Tip:** If working on a single package, build only that package to save time:
> ```bash
> colcon build --symlink-install --packages-select my_robot_description
> ```

---

## 📦 Packages and Modules

### 1. `my_robot_interfaces`
Contains custom message, service, and action specifications used across C++ and Python packages.

- **`msg/HardwareStatus.msg`**:
  ```text
  float64 temperature
  bool are_motors_ready
  string debug_message
  ```
- **`srv/ComputeRectangleArea.srv`**:
  ```text
  float64 length
  float64 width
  ---
  float64 area
  ```
- **`action/CountUntil.action`**:
  ```text
  # Goal
  int64 target_number
  float64 period
  ---
  # Result
  int64 reached_number
  ---
  # Feedback
  int64 current_number
  ```

---

### 2. `my_py_pkg` (Python Nodes)
Implemented with `rclpy`:
| Executable | Node Class | Description |
|---|---|---|
| `test_node` | `MyNode` | Minimal starter node test |
| `robot_news_station` | `PublisherNode` | Publishes status string to `/robot_news` (configurable `timer_period`) |
| `smartphone` | `SubscriberNode` | Subscribes to `/robot_news` and logs received messages |
| `add_two_ints_server` | `AddTwoIntsServerNode` | Service server handling `example_interfaces/srv/AddTwoInts` |
| `add_two_ints_client` | `AddTwoIntsClientNode` | Asynchronous service client calling `/add_two_ints` |
| `hardware_status_pub` | `HardwareStatusPublisher` | Publishes custom message `my_robot_interfaces/msg/HardwareStatus` to `/hardware_status` |
| `count_until_server` | `CountUntilServerNode` | Action server for `my_robot_interfaces/action/CountUntil` with cancellation and feedback |
| `count_until_client` | `CountUntilClientNode` | Action client sending goals, receiving feedback and results |

---

### 3. `my_cpp_pkg` (C++ Nodes)
Implemented with `rclcpp`:
| Executable | Description |
|---|---|
| `test_node` | Basic C++ OOP node skeleton |
| `robot_news_station` | String publisher to `/robot_news` |
| `smartphone` | String subscriber on `/robot_news` |
| `add_two_ints_server` | C++ Service server for `AddTwoInts` |
| `add_two_ints_client` | C++ Service client with asynchronous future handling |
| `hardware_status_pub` | Custom interface publisher (`HardwareStatus`) |
| `count_until_server` | Action server executing `CountUntil` action |
| `count_until_action_server_queue_goals` | Action server demonstrating mutex-protected **goal queuing** |
| `count_until_client` | Action client handling goal responses, feedback, and results |

---

### 4. `my_robot_description` (URDF & Simulation)
Mobile robot modeling and simulation package:
- **URDF / Xacro Files:**
  - `my_robot.urdf.xacro`: Main robot entry file including all subcomponents.
  - `common_properties.xacro`: Material definitions and inertial calculation macros (box, cylinder, sphere).
  - `mobile_base.xacro`: Differential drive mobile base with left/right drive wheels and caster wheel.
  - `mobile_base_gazebo.xacro`: Gazebo Sim plugins for `DiffDrive` and `JointStatePublisher`.
  - `camera.xacro`: Front-mounted camera link, optical frame, and Gazebo camera sensor plugin.
- **Launch Files:**
  - `display.launch.py`: Launches `robot_state_publisher`, `joint_state_publisher_gui`, and `rviz2`.
  - `gazebo.launch.py`: Launches Gazebo Sim with `test_world.sdf`, spawns robot, launches `ros_gz_bridge`, and opens RViz2.
- **Configurations:**
  - `config/gazebo_bridge.yaml`: Maps Gazebo topics (`gz.msgs`) to ROS 2 topics (`sensor_msgs`, `geometry_msgs`, `tf2_msgs`, `rosgraph_msgs`).
  - `worlds/test_world.sdf`: Gazebo simulation environment with lighting and obstacles.
  - `rviz/urdf_config.rviz`: RViz2 configuration pre-set with RobotModel, TF, and Camera display.

---

### 5. `my_robot_bringup` (Launch System)
Demonstrates multi-node orchestration and launch file configurations:
- `launch/start_comm.launch.py`:
  - Launches Python `robot_news_station` and C++ `smartphone`.
  - Demonstrates topic remapping (`/robot_news` -> `/my_news`).
  - Demonstrates parameter passing (`timer_period: 1.0`).

---

### 6. `executors_py` & `executors_cpp`
Demonstrates concurrency management in ROS 2:
- **`single_threaded_executor`**: Illustrates how long-running callbacks block other callbacks in the same node/thread.
- **`multi_threaded_executor`**: Shows how multiple threads execute callbacks concurrently using `ReentrantCallbackGroup` and thread pools.

---

### 7. `components_py` & `components_cpp`
Demonstrates node composition to reduce process overhead and enable intra-process zero-copy communication:
- `manual_composition`: Manually adding multiple nodes to a single executor inside one process.
- `number_pub_component`: Registering a C++ node as a shared library component (`rclcpp_components_register_nodes`) for dynamic composition into a component container.

---

## 💡 Tutorial Walkthrough & Running Examples

> **Note:** Remember to source your overlay in each new terminal:
> ```bash
> source install/setup.bash
> ```

### Publishers and Subscribers
Run the publisher and subscriber nodes (interoperable across C++ and Python):

```bash
# Terminal 1: Run Python publisher
ros2 run my_py_pkg robot_news_station

# Terminal 2: Run C++ subscriber
ros2 run my_cpp_pkg smartphone
```

---

### Services (Client / Server)
Test request-response communication:

```bash
# Terminal 1: Start service server (Python or C++)
ros2 run my_py_pkg add_two_ints_server

# Terminal 2: Call service using the client node
ros2 run my_py_pkg add_two_ints_client

# Or call directly from the CLI:
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 15, b: 27}"
```

---

### Custom Messages
Publish and monitor custom hardware status:

```bash
# Terminal 1: Run publisher
ros2 run my_py_pkg hardware_status_pub

# Terminal 2: Echo topic
ros2 topic echo /hardware_status
```

---

### Actions (Feedback & Goal Queuing)
Execute long-running goals with feedback and result reporting:

```bash
# Terminal 1: Start action server
ros2 run my_py_pkg count_until_server
# (Or run the C++ server with goal queueing: ros2 run my_cpp_pkg count_until_action_server_queue_goals)

# Terminal 2: Run action client
ros2 run my_py_pkg count_until_client

# Or trigger via CLI:
ros2 action send_goal /count_until my_robot_interfaces/action/CountUntil "{target_number: 10, period: 0.5}" --feedback
```

---

### Launch Files and Remapping
Start interconnected nodes with custom parameters and remapped topics:

```bash
ros2 launch my_robot_bringup start_comm.launch.py
```
Check the remapped topic:
```bash
ros2 topic list
# Output includes /my_news
```

---

### Executors & Concurrency
Observe single-threaded blocking vs. multi-threaded non-blocking execution:

```bash
# Python
ros2 run executors_py single_threaded_executor
ros2 run executors_py multi_threaded_executor

# C++
ros2 run executors_cpp single_threaded_executor
ros2 run executors_cpp multi_threaded_executor
```

---

### Component Composition
Execute composed nodes in a single process:

```bash
# Python manual composition
ros2 run components_py manual_composition

# C++ manual composition
ros2 run components_cpp manual_composition
```

---

### Robot Model in RViz2
Inspect the robot's kinematics, links, joints, and visual meshes:

```bash
ros2 launch my_robot_description display.launch.py
```
- Use the **Joint State Publisher GUI** slider to articulate robot joints.
- Inspect coordinate frames (`base_footprint`, `base_link`, wheels, `camera_link`, `camera_link_optical`).

---

### Robot Simulation in Gazebo Sim
Launch the full simulation environment with physics, sensors, bridge, and RViz2:

```bash
ros2 launch my_robot_description gazebo.launch.py
```

#### Teleoperating the Robot
In a separate terminal, drive the mobile robot using keyboard teleop:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/cmd_vel
```

#### Viewing Camera Stream
Open the image viewer to see the onboard simulated camera feed:

```bash
ros2 run rqt_image_view rqt_image_view /camera/image_raw
```

---

## 🌉 Gazebo Bridge Topics

The `my_robot_description/config/gazebo_bridge.yaml` configures bidirectional communication between Gazebo Sim and ROS 2:

| ROS 2 Topic | Gazebo Topic | Message Type | Direction |
|---|---|---|---|
| `/clock` | `/clock` | `rosgraph_msgs/msg/Clock` | Gazebo ➔ ROS 2 |
| `/joint_states` | `/world/empty/model/my_robot/joint_state` | `sensor_msgs/msg/JointState` | Gazebo ➔ ROS 2 |
| `/tf` | `/model/my_robot/tf` | `tf2_msgs/msg/TFMessage` | Gazebo ➔ ROS 2 |
| `/cmd_vel` | `/model/my_robot/cmd_vel` | `geometry_msgs/msg/Twist` | ROS 2 ➔ Gazebo |
| `/camera/camera_info` | `/camera/camera_info` | `sensor_msgs/msg/CameraInfo` | Gazebo ➔ ROS 2 |
| `/camera/image_raw` | `/camera/image_raw` | `sensor_msgs/msg/Image` | Gazebo ➔ ROS 2 |

---

## 🛠 Troubleshooting & Tips

- **Gazebo model does not appear or simulation crashes:**  
  Verify that your graphics drivers support OpenGL 3.3+ and that `ros-gz` is installed for your ROS 2 distro.
- **Node cannot find custom interface:**  
  Make sure you ran `source install/setup.bash` after building `my_robot_interfaces`.
- **Python script changes not reflecting:**  
  Use `colcon build --symlink-install` so that modifications to Python scripts in `src/` take effect immediately without rebuilding.

---

## 📄 License

This repository is distributed under the terms of the [Apache-2.0 License](LICENSE).
