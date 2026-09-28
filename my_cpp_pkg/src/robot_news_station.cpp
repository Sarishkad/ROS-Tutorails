#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

using namespace std::chrono_literals;
     
class PublisherNode : public rclcpp::Node 
{
public:
    PublisherNode() : Node("test_node") 
    {
        this->declare_parameter("timer_period", 1.0);
        double timer_period = this->get_parameter("timer_period").as_double();
        publisher_ = this->create_publisher<example_interfaces::msg::String>("robot_news", 10);
        timer_ = this->create_wall_timer(std::chrono::duration<double>(timer_period), std::bind(&PublisherNode::publishNews, this));
        RCLCPP_INFO(this->get_logger(), "robot news atation has been started");
    }

private:

    void publishNews()
    {
        auto msg = example_interfaces::msg::String();
        msg.data = "Hello from robot news station!";
        RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", msg.data.c_str());
        publisher_->publish(msg);
    }

    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PublisherNode>(); 
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}