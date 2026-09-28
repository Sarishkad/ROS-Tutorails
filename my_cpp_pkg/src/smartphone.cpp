#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

using namespace std::placeholders;

class SubscriberNode : public rclcpp::Node 
{
public:
    SubscriberNode() : Node("smartphone") 
    {
        SubscriberNode_ = this->create_subscription<example_interfaces::msg::String>(
            "robot_news", 10,
            std::bind(&SubscriberNode::callback_news, this, _1));

        RCLCPP_INFO(this->get_logger(), "Samrtphone node has been started");
    }

private:

    void callback_news(const example_interfaces::msg::String::SharedPtr msg)
    {
        RCLCPP_INFO(this->get_logger(), "Received news: '%s'", msg->data.c_str());
    }

    rclcpp::Subscription<example_interfaces::msg::String>::SharedPtr SubscriberNode_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SubscriberNode>(); 
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}