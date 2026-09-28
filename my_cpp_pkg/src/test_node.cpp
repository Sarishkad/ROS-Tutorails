#include "rclcpp/rclcpp.hpp"
     
class TestNode : public rclcpp::Node 
{
public:
    TestNode() : Node("test_node") 
    {
        RCLCPP_INFO(this->get_logger(), "Hello World!");
        timer_ = this->create_wall_timer(std::chrono::seconds(1),
                                         std::bind(&TestNode::timerCallback, this));
    }

private:

    void timerCallback()
    {
        RCLCPP_INFO(this->get_logger(), "Hello ROS2 %d", counter_);
        counter_ = counter_ + 1;
    }

    rclcpp::TimerBase::SharedPtr timer_;
    int counter_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TestNode>(); 
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}