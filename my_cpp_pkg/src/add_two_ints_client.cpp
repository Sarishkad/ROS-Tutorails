#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"
     
using namespace std::chrono_literals;

class AddTwoIntsClientNode : public rclcpp::Node 
{
public:
    AddTwoIntsClientNode() : Node("add_two_ints_client_node") 
    {
        RCLCPP_INFO(this->get_logger(), "Client Node Started!");
        client_ = this->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");
    }

    void call_add_two_ints(int a, int b)
    {

        while(!client_->wait_for_service(1s))
        {
            RCLCPP_INFO(this->get_logger(), "Waiting for service to be available...");
        }
        auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
        request->a = a;
        request->b = b;

        client_->async_send_request(
            request, std::bind(
            &AddTwoIntsClientNode::callback_call_add_two_ints, 
            this, 
            std::placeholders::_1));
    }
    
private:
    void callback_call_add_two_ints(rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture future)
        {
            auto response = future.get();
            RCLCPP_INFO(this->get_logger(), "Result: %d ", (int)response->sum);
        }

        rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<AddTwoIntsClientNode>();
    node->call_add_two_ints(6, 4);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}