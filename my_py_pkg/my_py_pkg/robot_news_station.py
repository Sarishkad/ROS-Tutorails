#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String


class PublisherNode(Node):  
    def __init__(self):
        super().__init__("robot_news_station")
        self.declare_parameter("timer_period", 1.0)
        self.timer_period = self.get_parameter("timer_period").value
        self.publisher_ = self.create_publisher(String, "robot_news", 10)
        self.timer_ = self.create_timer(self.timer_period, self.publish_news)
        self.get_logger().info("Robot News Station Node has been started.")
        
    def publish_news(self):
        msg = String()
        msg.data = "Hello, from the Robot News Station!"
        self.publisher_.publish(msg)
        self.get_logger().info(f"Published: {msg.data}")


def main(args=None):
    rclpy.init(args=args)
    node = PublisherNode()  
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
