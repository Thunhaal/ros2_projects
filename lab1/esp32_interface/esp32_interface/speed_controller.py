import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from std_msgs.msg import Int32


class SpeedController(Node):

    def __init__(self):
        super().__init__('speed_controller')

        self.subscription = self.create_subscription(
            Float32,
            '/ultrasonic',
            self.ultrasonic_callback,
            10
        )

        self.publisher = self.create_publisher(
            Int32,
            '/motor_cmd',
            10
        )

        self.get_logger().info("Speed Controller Started")


    def ultrasonic_callback(self, msg):

        distance = msg.data

        if distance <= 10:
            pwm = 0

        elif distance >= 50:
            pwm = 255

        else:
            pwm = int((distance - 10) * 255 / 40)

        motor_msg = Int32()
        motor_msg.data = pwm

        self.publisher.publish(motor_msg)

        self.get_logger().info(
            f"Distance: {distance:.2f} cm   PWM: {pwm}"
        )


def main(args=None):

    rclpy.init(args=args)

    node = SpeedController()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
